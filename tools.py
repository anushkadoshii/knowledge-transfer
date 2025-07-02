import requests
import spacy
from typing import List, Dict
import os
import tempfile
from pathlib import Path
from crewai.tools import BaseTool
from utils.github_utils import fetch_user_repos, fetch_repo_commits

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

    def _run(self, email_id: str, password: str, limit: int = 10) -> List[Dict]:
        """Fetch recent emails (placeholder implementation)."""
        return [{
            "subject": f"Email {i+1}",
            "from": "sender@example.com",
            "date": "2025-07-01",
            "body": f"This is sample email content {i+1}"
        } for i in range(limit)]

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

    def _run(self, file_data: List[Dict]) -> List[Dict]:
        """Extract text from files (placeholder implementation)."""
        return [{
            "filename": file["filename"],
            "content": f"Extracted text sample from {file['filename']}"
        } for file in file_data]

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

