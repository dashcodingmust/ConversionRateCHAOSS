import requests
from datetime import datetime, timedelta, timezone
from backend.src.config import HEADERS


def pr_metrics(owner, repo, days=90):
    page = 1
    merged = 0
    total_closed = 0

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {
            "state": "closed",
            "per_page": 100,
            "page": page,
            "sort": "updated",
            "direction": "desc"
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=10
        )
        print("Requesting URL:", url)
        print("Owner:", owner)
        print("Repo:", repo)

        if response.status_code != 200:
            break 

        data = response.json()

        if not data:
            break

        for pr in data:
            closed_at = datetime.fromisoformat(
                pr["closed_at"].replace("Z", "+00:00")
            )

            # Stop if PR older than cutoff
            if closed_at < cutoff_date:
                continue

            total_closed += 1

            if pr.get("merged_at") is not None:
                merged += 1

        page += 1
        print("Merged:", merged)
        print("Total Closed:", total_closed)

    return finalize_metrics(merged, total_closed)


def finalize_metrics(merged, total_closed):
    if total_closed == 0:
        return {
            "merge_rate": 0,
            "avg_merge_time_days": 0
        }

    merge_rate = round((merged / total_closed) * 100, 2)

    return {
        "merge_rate": merge_rate,
        "avg_merge_time_days": 0  # Can re-add time logic later
    }