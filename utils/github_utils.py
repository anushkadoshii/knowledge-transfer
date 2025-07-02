import requests
from typing import Optional, List, Dict

def parse_github_username(user_input: str) -> str:
    if user_input.startswith("http"):
        path = urlparse(user_input).path
        username = path.strip("/").split("/")[0]
        return username
    return user_input.strip()

def get_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    return headers

def fetch_user_repos(github_username: str, token: str = None) -> List[Dict]:
    url = f"https://api.github.com/users/{github_username}/repos"
    headers = {"Authorization": f"token {token}"} if token else {}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_repo_commits(github_username: str, repo_name: str, token: str = None, per_page: int = 30, max_pages: int = 2) -> List[Dict]:
    commits = []
    for page in range(1, max_pages + 1):
        url = f"https://api.github.com/repos/{github_username}/{repo_name}/commits"
        params = {"per_page": per_page, "page": page}
        headers = {"Authorization": f"token {token}"} if token else {}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            break
        page_commits = response.json()
        if not page_commits:
            break
        commits.extend(page_commits)
    return commits

def parse_commit_data(commit_json: Dict) -> Dict:
    return {
        "sha": commit_json.get("sha"),
        "author": commit_json.get("commit", {}).get("author", {}).get("name"),
        "date": commit_json.get("commit", {}).get("author", {}).get("date"),
        "message": commit_json.get("commit", {}).get("message"),
        "url": commit_json.get("html_url"),
    }

def fetch_all_user_commits(user_input: str, token: Optional[str] = None, per_page: int = 30, max_pages: int = 2) -> List[Dict]:
    username = parse_github_username(user_input)
    repos = fetch_user_repos(username, token)
    all_commits = []
    for repo in repos:
        repo_name = repo["name"]
        commits = fetch_repo_commits(username, repo_name, token, per_page, max_pages)
        for commit in commits:
            all_commits.append(parse_commit_data(commit))
    return all_commits
