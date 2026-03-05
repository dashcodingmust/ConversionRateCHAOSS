import requests
from backend.src.config import HEADERS
def last_commit_time(limit, owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    response =requests.get(url, headers=HEADERS)

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        return "No commit data found"

    last_commit = data[0]

    return last_commit["commit"]["committer"]["date"]