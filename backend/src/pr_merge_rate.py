import requests
from backend.src.config import GITHUB_TOKEN
def pr_merge_rate(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed"
    HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}"
}
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    if not isinstance(data, list):
        return 0

    merged = 0
    total = 0

    for pr in data:

        try:
            total += 1

            if pr["merged_at"] is not None:
                merged += 1

        except:
            continue

    if total == 0:
        return 0

    return round((merged / total) * 100, 2)