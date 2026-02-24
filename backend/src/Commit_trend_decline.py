import requests
from datetime import datetime, timedelta

def get_commit_count(owner, repo, since, until):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    params = {
        "since": since,
        "until": until,
        "per_page": 100
    }

    response = requests.get(url, params=params)
    return len(response.json())


def commit_trend(owner, repo):

    now = datetime.utcnow()
    last_30 = now - timedelta(days=30)
    prev_30 = now - timedelta(days=60)

    recent = get_commit_count(owner, repo, last_30.isoformat(), now.isoformat())
    previous = get_commit_count(owner, repo, prev_30.isoformat(), last_30.isoformat())

    print("\n📉 Commit Trend Analysis")
    print("-------------------------")
    print("Commits last 30 days:", recent)
    print("Commits previous 30 days:", previous)

    if previous == 0:
        print("Not enough past data.")
        return

    change = ((recent - previous) / previous) * 100

    print("Change:", round(change, 2), "%")

    if change > 0:
        print("Trend: Growing 📈")
    elif change >= -20:
        print("Trend: Stable 👍")
    elif change >= -50:
        print("Trend: Declining ⚠")
    else:
        print("Trend: Serious Decline 🚨")