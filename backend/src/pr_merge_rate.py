import requests
from datetime import datetime
from backend.src.config import HEADERS


def pr_metrics(owner, repo):
    page = 1
    merged = 0
    total_closed = 0
    total_merge_time_days = 0

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        params = {
            "state": "closed",
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
            return {
                "merge_rate": 0,
                "avg_merge_time_days": 0
            }

        data = response.json()

        if not data:
            break

        for pr in data:
            total_closed += 1

            if pr.get("merged_at") is not None:
                merged += 1

                created_at = datetime.fromisoformat(
                    pr["created_at"].replace("Z", "+00:00")
                )
                merged_at = datetime.fromisoformat(
                    pr["merged_at"].replace("Z", "+00:00")
                )

                merge_time = (merged_at - created_at).days
                total_merge_time_days += merge_time

        page += 1

    if total_closed == 0:
        return {
            "merge_rate": 0,
            "avg_merge_time_days": 0
        }

    merge_rate = round((merged / total_closed) * 100, 2)

    avg_merge_time = (
        round(total_merge_time_days / merged, 2)
        if merged > 0 else 0
    )

    return {
        "merge_rate": merge_rate,
        "avg_merge_time_days": avg_merge_time
    }