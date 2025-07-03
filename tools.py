import requests
import spacy
from typing import List, Dict
import os
import tempfile
from pathlib import Path
from crewai.tools import BaseTool
from io import BytesIO
from utils.github_utils import fetch_user_repos, fetch_repo_commits
from utils.file_utils import extract_text_from_file
from utils.email_utils import get_all_relevant_emails

# Initialize NLP model (ensure the model is installed via requirements.txt)
nlp = spacy.load("en_core_web_sm")

class GitHubCommitsTool(BaseTool):
    name: str = "GitHub Commits Fetcher"
    description: str = "Fetches commit history for a GitHub user."

    def _run(self, github_username: str, token: str = None) -> List[Dict]:
        """Fetch commit history for a GitHub user using github_utils."""
        commits = []
        repos = fetch_user_repos(github_username, token)
        for repo in repos:
            if not isinstance(repo, dict) or "name" not in repo:
                continue
            repo_name = repo["name"]
            repo_commits = fetch_repo_commits(github_username, repo_name, token)
            if isinstance(repo_commits, list):
                commits.extend(repo_commits)
        return commits[:50]

class EmailProcessorTool(BaseTool):
    name: str = "Email Processor"
    description: str = "Processes and summarizes email content." 
    
    def _run(self, person_name: str, mapping: dict, company_domain: str) -> dict:
        """
        Fetch emails as per requirements:
        - All company emails to/from user
        - All emails with attachments
        """
        try:
            email_data = get_all_relevant_emails(person_name, mapping, company_domain)
            # You can further process or summarize email_data here if needed
            return {
                "from_company": [
                    {"subject": msg.subject, "from": msg.from_, "to": msg.to, "date": msg.date}
                    for msg in email_data["from_company"]
                ],
                "to_company": [
                    {"subject": msg.subject, "from": msg.from_, "to": msg.to, "date": msg.date}
                    for msg in email_data["to_company"]
                ],
                "with_attachments": [
                    {"subject": msg.subject, "from": msg.from_, "to": msg.to, "date": msg.date, "attachments": [att.filename for att in msg.attachments]}
                    for msg in email_data["with_attachments"]
                ]
            }
        except Exception as e:
            return {"error": str(e)}

class FileProcessorTool(BaseTool):
    name: str = "File Processor"
    description: str = "Processes uploaded files and extracts metadata."

    def _run(self, uploaded_files: List) -> List[Dict]:
        """Process uploaded files and extract metadata."""
        return [{
            "filename": file.name,
            "filetype": file.type,
            "size": len(file.getvalue())
        } for file in uploaded_files]

class DocumentTextExtractorTool(BaseTool):
    name: str = "Document Text Extractor"
    description: str = "Extracts text from documents, slides, and sheets."

    def _run(self, uploaded_files: List) -> List[Dict]:
        """
        Extract text from Streamlit-uploaded files.
        Each file is a Streamlit UploadedFile object.
        """
        results = []
        for file in uploaded_files:
            filename = file.name
            file_stream = BytesIO(file.getvalue())
            try:
                text = extract_text_from_file(filename, file_stream)
            except Exception as e:
                text = f"Error extracting text: {str(e)}"
            results.append({
                "filename": filename,
                "content": text
            })
        return results


class NLPAnalyzerTool(BaseTool):
    name: str = "NLP Analyzer"
    description: str = "Performs NLP analysis including entity recognition and summarization."

    def _run(self, texts: List[str]) -> List[Dict]:
        """Perform NLP analysis on text."""
        results = []
        for text in texts:
            doc = nlp(text)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            summary = text[:200] + "..." if len(text) > 200 else text
            results.append({
                "entities": entities,
                "summary": summary,
                "topics": ["topic1", "topic2"]  # Placeholder
            })
        return results

class KnowledgeBaseBuilderTool(BaseTool):
    name: str = "Knowledge Base Builder"
    description: str = "Builds structured knowledge base from extracted insights."

    def _run(self, insights: List[Dict]) -> Dict:
        """Build knowledge base from insights."""
        return {
            "entities": [item for insight in insights for item in insight.get("entities", [])],
            "summaries": [insight.get("summary", "") for insight in insights],
            "topics": list(set([topic for insight in insights for topic in insight.get("topics", [])]))
        }

# Optional: Export tool instances if you prefer to use them directly in agents.py
# But you can also instantiate them directly in agents.py as shown in the example below.

