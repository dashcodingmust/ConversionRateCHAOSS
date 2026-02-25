import requests
from datetime import datetime, timedelta

def active_maintainers(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = requests.get(url, params={"per_page": 100})
    commits = response.json()

    cutoff = datetime.utcnow() - timedelta(days=30)

    maintainers = set()

    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        commit_date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")

        if commit_date >= cutoff:
            if commit["author"]:
                maintainers.add(commit["author"]["login"])

    count = len(maintainers)

    # determine status
    if count >= 5:
        status = "Excellent"
    elif count >= 3:
        status = "Healthy"
    elif count == 2:
        status = "Risk"
    else:
        status = "High Risk"

    return {
        "active_maintainers": count,
        "status": status
    }
