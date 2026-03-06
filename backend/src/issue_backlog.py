import httpx
from datetime import datetime, timedelta, timezone
from config import HEADERS


async def issue_backlog(owner, repo, days=90):

    page = 1
    open_issues = 0
    recently_closed = 0

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)

    async with httpx.AsyncClient() as client:
        while True:
            url = f"https://api.github.com/repos/{owner}/{repo}/issues"
            params = {
                "state": "open",
                "per_page": 100,
            "page": page
        }

            response = await client.get(
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

   
        page = 1
        
        while True:
            url = f"https://api.github.com/repos/{owner}/{repo}/issues"
            params = {
                "state": "closed",
                "per_page": 100,
                "page": page,
                "sort": "updated",
                "direction": "desc"
            }

            response = await client.get(
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
                if "pull_request" in item:
                    continue

                closed_at = datetime.fromisoformat(
                    item["closed_at"].replace("Z", "+00:00")
                )

                if closed_at >= cutoff:
                    recently_closed += 1

            page += 1

    backlog_ratio = (
        round(open_issues / recently_closed, 2)
        if recently_closed > 0 else 0
    )

    return {
        "open_issues": open_issues,
        "recently_closed_issues": recently_closed,
        "issue_backlog_ratio": backlog_ratio
    }