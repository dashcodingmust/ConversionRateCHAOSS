import requests
from config import HEADERS
def backlog_status(issue_count):
    if issue_count <= 20:
        return "Healthy"
    elif issue_count <= 100:
        return "Moderate"
    elif issue_count <= 500:
        return "High"
    else:
        return "Critical"


def issue_backlog(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"
    
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # safety check (rate limit / invalid repo)
    if "open_issues_count" not in data:
        return {
            "open_issues": 0,
            "status": "API Error"
        }

    open_issues = data["open_issues_count"]
    status = backlog_status(open_issues)

    return {
        "open_issues": open_issues,
        "status": status
    }