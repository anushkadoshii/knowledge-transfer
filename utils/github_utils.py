import requests
from typing import List, Dict


def fetch_user_repos(github_username: str, token: str = None) -> List[Dict]:
    url = f"https://api.github.com/users/{github_username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_repo_commits(github_username: str, repo_name: str, token: str = None) -> List[Dict]:
    url = f"https://api.github.com/repos/{github_username}/{repo_name}/commits"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()
