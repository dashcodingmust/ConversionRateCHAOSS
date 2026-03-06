import httpx
from datetime import datetime, timedelta, timezone
from config import HEADERS


MAX_PAGES = 20  

async def pr_metrics(owner, repo, days=90):

    page = 1
    merged = 0
    total_closed = 0
    total_merge_time_days = 0

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    async with httpx.AsyncClient() as client:

        while page <= MAX_PAGES:

            url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
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

            all_older_than_cutoff = True

            for pr in data:

                closed_at = datetime.fromisoformat(
                    pr["closed_at"].replace("Z", "+00:00")
                )

                if closed_at >= cutoff_date:
                    all_older_than_cutoff = False
                    total_closed += 1

                    if pr.get("merged_at") is not None:
                        merged += 1

                        created_at = datetime.fromisoformat(
                            pr["created_at"].replace("Z", "+00:00")
                        )
                        merged_at = datetime.fromisoformat(
                            pr["merged_at"].replace("Z", "+00:00")
                        )

                        merge_time_days = (merged_at - created_at).days
                        total_merge_time_days += merge_time_days

            if all_older_than_cutoff:
                break

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



async def pr_backlog(owner, repo, days=90):

    page = 1
    open_prs = 0
    recently_closed = 0

    cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)

    async with httpx.AsyncClient() as client:

        while page <= MAX_PAGES:

            url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
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

            open_prs += len(data)
            page += 1

        page = 1

        while page <= MAX_PAGES:

            url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
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

            all_older_than_cutoff = True

            for pr in data:

                closed_at = datetime.fromisoformat(
                    pr["closed_at"].replace("Z", "+00:00")
                )

                if closed_at >= cutoff_date:
                    all_older_than_cutoff = False
                    recently_closed += 1

            if all_older_than_cutoff:
                break

            page += 1

    backlog_ratio = (
        round(open_prs / recently_closed, 2)
        if recently_closed > 0 else 0
    )

    return {
        "open_prs": open_prs,
        "recently_closed_prs": recently_closed,
        "backlog_ratio": backlog_ratio
    }