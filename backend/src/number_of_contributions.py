import httpx
from config import get_headers


async def investment(owner, repo, threshold):
    MAX_PAGES = 5  # 500 contributors is more than enough for conversion rate
    contributors = []
    page = 1

    async with httpx.AsyncClient() as client:
        while page <= MAX_PAGES:
            url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"
            response = await client.get(url, headers=get_headers())

            if response.status_code != 200:
                return {"conversion_rate": 0, "status": "API error"}

            data = response.json()

            if not data:
                break

            contributors.extend(data)
            page += 1

    contributors = [
        c for c in contributors if c.get("type") == "User"
    ]

    total_contributors = len(contributors)

    if total_contributors == 0:
        return {"conversion_rate": 0, "stage_distribution": {"D0": 0, "D1": 0, "D2": 0}}

    stage_counts = {"D0": 0, "D1": 0, "D2": 0}

    for c in contributors:
        contributions = c["contributions"]

        if contributions <= 20:
            stage_counts["D0"] += 1
        elif contributions < threshold:
            stage_counts["D1"] += 1
        else:
            stage_counts["D2"] += 1

    conversion_rate = round(
        (stage_counts["D2"] / total_contributors) * 100, 2
    )

    return {
        "conversion_rate": conversion_rate,
        "stage_distribution": stage_counts
    }