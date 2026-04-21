import httpx
from datetime import datetime, timedelta, timezone
<<<<<<< HEAD
from config import HEADERS


async def active_maintainers(owner, repo, days=90):
    MAX_PAGES = 15
=======
from config import get_headers


async def active_maintainers(owner, repo, days=90):
    MAX_PAGES = 5  # commits filtered by `since`, 500 is plenty
>>>>>>> master
    page = 1
    maintainers = set()

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
<<<<<<< HEAD
=======
    since = cutoff.isoformat()

>>>>>>> master
    async with httpx.AsyncClient() as client:

        while page <= MAX_PAGES:
            url = f"https://api.github.com/repos/{owner}/{repo}/commits"
            params = {
<<<<<<< HEAD
=======
                "since": since,
>>>>>>> master
                "per_page": 100,
                "page": page
            }

            response = await client.get(
                url,
<<<<<<< HEAD
                headers=HEADERS,
=======
                headers=get_headers(),
>>>>>>> master
                params=params,
                timeout=10
            )

            if response.status_code != 200:
                break

            data = response.json()

            if not data:
                break

            for commit in data:
<<<<<<< HEAD
                commit_date_str = commit["commit"]["author"]["date"]
                commit_date = datetime.fromisoformat(
                    commit_date_str.replace("Z", "+00:00")
                )

                if commit_date < cutoff:
                    continue

=======
>>>>>>> master
                if commit.get("author") and commit["author"].get("login"):
                    maintainers.add(commit["author"]["login"])

            page += 1

<<<<<<< HEAD
    return len(maintainers)
=======
    return len(maintainers)
>>>>>>> master
