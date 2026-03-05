import requests
import pandas as pd
from backend.src.config import HEADERS


# classify contributor
def stage(x, threshold):
    if x == 1:
        return "D0"          # one-time contributor
    elif x >= threshold:
        return "D2"          # regular contributor
    else:
        return "D1"          # occasional contributor


def investment(owner, repo, threshold=20):

    # request more contributors
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"

    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
    except Exception:
        return {"conversion_rate": 0, "status": "API error"}

    if not isinstance(data, list) or len(data) == 0:
        return {"conversion_rate": 0, "status": "API error"}

    contributors = pd.DataFrame(data)[["login", "contributions"]]

    contributors["investment"] = contributors["contributions"].apply(
        lambda x: stage(x, threshold)
    )

    total_contributors = len(contributors)
    total_regular = (contributors["investment"] == "D2").sum()

    # convert to percentage
    conversion_rate = round((total_regular / total_contributors) * 100, 2)

    return {"conversion_rate": conversion_rate}