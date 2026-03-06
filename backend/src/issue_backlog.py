import requests
from datetime import datetime, timedelta, timezone
from config import HEADERS


def issue_backlog(owner, repo):

    page = 1
    open_issues = 0
    recently_closed = 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        params = {
            "state": "open",
            "per_page": 100,
            "page": page
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        if response.status_code != 200:
            break

        data = response.json()

        if not data:
            break

        for item in data:
            if "pull_request" not in item:
                open_issues += 1

        page += 1

        return {
        "open_issues": open_issues
    }