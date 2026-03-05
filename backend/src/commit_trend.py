import requests
from datetime import datetime, timedelta
from backend.src.config import HEADERS

def get_commit_count(owner, repo, since, until):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "since": since,
        "until": until,
        "per_page": 100
    }

    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if not isinstance(data, list):
        return 0

    return len(data)


def commit_trend(owner, repo):

    now = datetime.utcnow()
    last_30 = now - timedelta(days=30)
    prev_30 = now - timedelta(days=60)

    recent = get_commit_count(owner, repo, last_30.isoformat(), now.isoformat())
    previous = get_commit_count(owner, repo, prev_30.isoformat(), last_30.isoformat())

    if previous == 0:
        return {
            "recent_commits": recent,
            "previous_commits": previous,
            "change_percent": None,
            "trend": "Not enough past data"
        }

    change = ((recent - previous) / previous) * 100

    if change > 0:
        trend = "Growing"
    elif change >= -20:
        trend = "Stable"
    elif change >= -50:
        trend = "Declining"
    else:
        trend = "Serious Decline"

    return {
        "recent_commits": recent,
        "previous_commits": previous,
        "change_percent": round(change, 2),
        "trend": trend
    }