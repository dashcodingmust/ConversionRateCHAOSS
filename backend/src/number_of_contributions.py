import requests
import pandas as pd
from backend.src.config import HEADERS


def stage(x, threshold):
    if x <= 1:
        return "D0"          
    elif x >= threshold:
        return "D2"         
    else:
        return "D1"          


def investment(owner, repo, threshold):
    contributors = []
    page = 1

    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100&page={page}"
        response = requests.get(url, headers=HEADERS)

        if response.status_code != 200:
            return {"conversion_rate": 0, "status": "API error"}

        data = response.json()

        if not data:
            break

        contributors.extend(data)
        page += 1

    # Filter only real users
    contributors = [
        c for c in contributors if c.get("type") == "User"
    ]

    total_contributors = len(contributors)

    total_regular = sum(
        1 for c in contributors if c["contributions"] >= threshold
    )

    if total_contributors == 0:
        return {"conversion_rate": 0}

    conversion_rate = round(
        (total_regular / total_contributors) * 100, 2
    )

    return {"conversion_rate": conversion_rate}