import requests
from datetime import datetime, timedelta
from backend.src.config import GITHUB_TOKEN

def active_maintainers(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
    }
    response = requests.get(url, headers=HEADERS)

    data = response.json()

    if not isinstance(data, list):
        return "GitHub API error"

    cutoff = datetime.utcnow() - timedelta(days=90)
    maintainers = set()

    for commit in data:

        try:
            date_str = commit["commit"]["author"]["date"]
            date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

            if date > cutoff:
                maintainers.add(commit["commit"]["author"]["name"])

        except:
            continue

    return len(maintainers)