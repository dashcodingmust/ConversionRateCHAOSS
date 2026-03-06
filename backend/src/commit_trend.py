import requests
from datetime import datetime, timedelta
from collections import defaultdict
from backend.src.config import HEADERS


def commit_trend(owner, repo, days=90):
    now = datetime.utcnow()
    since = (now - timedelta(days=days)).isoformat()

    page = 1
    commits = []

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        params = {
            "since": since,
            "per_page": 100,
            "page": page
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )

        if response.status_code == 403:
            return {"status": "Rate limit exceeded"}

        if response.status_code != 200:
            return {"status": "API error"}

        data = response.json()

        if not data:
            break

        commits.extend(data)
        page += 1

    weekly_counts = defaultdict(int)

    for commit in commits:
        date_str = commit["commit"]["author"]["date"]
        date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))

        week_start = date_obj - timedelta(days=date_obj.weekday())
        week_label = week_start.strftime("%Y-%m-%d")

        weekly_counts[week_label] += 1

    # Generate full week timeline
    start_date = now - timedelta(days=days)
    current_week = start_date - timedelta(days=start_date.weekday())

    all_weeks = []
    while current_week <= now:
        week_label = current_week.strftime("%Y-%m-%d")
        all_weeks.append(week_label)
        current_week += timedelta(days=7)

    commit_counts = [weekly_counts.get(week, 0) for week in all_weeks]

    return {
        "labels": all_weeks,
        "commit_counts": commit_counts
    }