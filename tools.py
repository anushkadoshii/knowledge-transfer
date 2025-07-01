import requests
import spacy
from typing import List, Dict
import os
import tempfile
from pathlib import Path
from crewai import tool

# Initialize NLP model
nlp = spacy.load("en_core_web_sm")

@tool("GitHub Commits Fetcher")
def fetch_user_commits(github_username: str, token: str = None) -> List[Dict]:
    """Fetch commit history for a GitHub user."""
    url = f"https://api.github.com/users/{github_username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    repos = requests.get(url, headers=headers).json()
    commits = []
    for repo in repos:
        if not isinstance(repo, dict) or "name" not in repo:
            continue
        repo_name = repo["name"]
        commits_url = f"https://api.github.com/repos/{github_username}/{repo_name}/commits"
        repo_commits = requests.get(commits_url, headers=headers).json()
        if isinstance(repo_commits, list):
            commits.extend(repo_commits)
    return commits[:50]

@tool("Email Processor")
def fetch_emails(email_id: str, password: str, limit: int = 10) -> List[Dict]:
    """Fetch recent emails (placeholder implementation)."""
    return [{
        "subject": f"Email {i+1}",
        "from": "sender@example.com",
        "date": "2025-07-01",
        "body": f"This is sample email content {i+1}"
    } for i in range(limit)]

@tool("File Processor")
def process_uploaded_files(uploaded_files: List) -> List[Dict]:
    """Process uploaded files and extract metadata."""
    return [{
        "filename": file.name,
        "filetype": file.type,
        "size": len(file.getvalue())
    } for file in uploaded_files]

@tool("Document Text Extractor")
def extract_text_from_files(file_data: List[Dict]) -> List[Dict]:
    """Extract text from files (placeholder implementation)."""
    return [{
        "filename": file["filename"],
        "content": f"Extracted text sample from {file['filename']}"
    } for file in file_data]

@tool("NLP Analyzer")
def analyze_text(texts: List[str]) -> List[Dict]:
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

@tool("Knowledge Base Builder")
def build_knowledge_base(insights: List[Dict]) -> Dict:
    """Build knowledge base from insights."""
    return {
        "entities": [item for insight in insights for item in insight.get("entities", [])],
        "summaries": [insight.get("summary", "") for insight in insights],
        "topics": list(set([topic for insight in insights for topic in insight.get("topics", [])]))
    }
