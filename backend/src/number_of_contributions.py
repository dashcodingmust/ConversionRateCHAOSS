import requests
import pandas as pd

# classify contributor
def stage(x, threshold):
    if x == 1:
        return "D0"
    elif x >= threshold:
        return "D2"
    else:
        return "D1"


def investment(owner, repo, threshold=5):

    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    response = requests.get(url)
    data = response.json()

    if not isinstance(data, list) or len(data) == 0:
        return {"conversion_rate": 0, "status": "API error"}

    contributors = pd.DataFrame(data)[["login", "contributions"]]

    contributors["investment"] = contributors["contributions"].apply(
        lambda x: stage(x, threshold)
    )

    total_D2 = (contributors["investment"] == "D2").sum()
    conversion_rate = round(total_D2 / len(contributors), 2)

    return {"conversion_rate": conversion_rate}