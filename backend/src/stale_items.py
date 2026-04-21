import httpx
from datetime import datetime, timedelta, timezone
from config import get_headers

MAX_PAGES = 8  # 800 open items is a reasonable ceiling
STALE_DAYS = 30


async def stale_items(owner, repo, days=90):
    cutoff = datetime.now(timezone.utc) - timedelta(days=STALE_DAYS)

    stale_prs = []
    stale_issues = []

    async with httpx.AsyncClient() as client:

        # --- Stale open PRs ---
        # Sorted by updated asc: once we see a PR newer than cutoff, all later pages are fresh too.
        page = 1
        while page <= MAX_PAGES:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/pulls",
                headers=get_headers(),
                params={"state": "open", "per_page": 100, "page": page, "sort": "updated", "direction": "asc"},
                timeout=10,
            )
            if response.status_code != 200 or not response.json():
                break
            found_fresh = False
            for pr in response.json():
                updated_at = datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00"))
                if updated_at < cutoff:
                    stale_prs.append({
                        "number": pr["number"],
                        "title": pr["title"],
                        "url": pr["html_url"],
                        "days_stale": (datetime.now(timezone.utc) - updated_at).days,
                        "author": pr["user"]["login"],
                    })
                else:
                    found_fresh = True
                    break
            if found_fresh:
                break
            page += 1

        # --- Stale open issues ---
        # Same logic: sorted updated asc, break once we hit a fresh item.
        page = 1
        while page <= MAX_PAGES:
            response = await client.get(
                f"https://api.github.com/repos/{owner}/{repo}/issues",
                headers=get_headers(),
                params={"state": "open", "per_page": 100, "page": page, "sort": "updated", "direction": "asc"},
                timeout=10,
            )
            if response.status_code != 200 or not response.json():
                break
            found_fresh = False
            for item in response.json():
                if "pull_request" in item:
                    continue
                updated_at = datetime.fromisoformat(item["updated_at"].replace("Z", "+00:00"))
                if updated_at < cutoff:
                    stale_issues.append({
                        "number": item["number"],
                        "title": item["title"],
                        "url": item["html_url"],
                        "days_stale": (datetime.now(timezone.utc) - updated_at).days,
                        "author": item["user"]["login"],
                    })
                else:
                    found_fresh = True
                    break
            if found_fresh:
                break
            page += 1

    # Sort by most stale first
    stale_prs.sort(key=lambda x: x["days_stale"], reverse=True)
    stale_issues.sort(key=lambda x: x["days_stale"], reverse=True)

    return {
        "stale_prs": stale_prs[:10],
        "stale_issues": stale_issues[:10],
        "stale_pr_count": len(stale_prs),
        "stale_issue_count": len(stale_issues),
    }
