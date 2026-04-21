import httpx
from datetime import datetime, timedelta, timezone
from config import get_headers


async def active_maintainers(owner, repo, days=90):
    MAX_PAGES = 5  # commits filtered by `since`, 500 is plenty
    page = 1
    maintainers = set()

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    since = cutoff.isoformat()

    async with httpx.AsyncClient() as client:

        while page <= MAX_PAGES:
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            params = {
                "since": since,
                "per_page": 100,
                "page": page
            }

            response = await client.get(
                url,
                headers=get_headers(),
                params=params,
                timeout=10
            )

            if response.status_code != 200:
                break

            data = response.json()

            if not data:
                break

            for commit in data:
                if commit.get("author") and commit["author"].get("login"):
                    maintainers.add(commit["author"]["login"])

            page += 1

    return len(maintainers)
