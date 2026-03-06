import httpx
from datetime import datetime, timezone
from config import HEADERS


async def last_commit_time(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"

    async with httpx.AsyncClient() as client:
        response = await client.get(
            url,
            headers=HEADERS,
            timeout=10
        )

    if response.status_code != 200:
        return {"status": "API error"}

    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        return {"status": "No commit data found"}

    last_commit = data[0]
    commit_date_str = last_commit["commit"]["committer"]["date"]

    commit_date = datetime.fromisoformat(
        commit_date_str.replace("Z", "+00:00")
    )

    now = datetime.now(timezone.utc)
    days_since = (now - commit_date).days

    return {
        "last_commit_date": commit_date_str,
        "days_since_last_commit": days_since
    }