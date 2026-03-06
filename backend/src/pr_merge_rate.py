import requests
from backend.src.config import HEADERS


def pr_merge_rate(owner, repo):
    page = 1
    merged = 0
    total = 0

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

        if response.status_code == 403:
            return 0

        if response.status_code != 200:
            return 0

        data = response.json()

        if not data:
            break

        for pr in data:
            total += 1
            if pr.get("merged_at") is not None:
                merged += 1

        page += 1

    if total == 0:
        return 0

    return round((merged / total) * 100, 2)