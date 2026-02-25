import requests

def pr_merge_rate(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}/pulls?state=closed&per_page=100"
    response = requests.get(url)
    pulls = response.json()

    if not pulls:
        print("No pull requests found.")
        return

    merged = 0

    for pr in pulls:
        if pr["merged_at"] is not None:
            merged += 1

    total = len(pulls)
    rate = merged / total * 100

    return {"Pull Request Merge Report",
           "----------------------------",
           "Closed PRs analyzed:": total,
           "Merged PRs:": merged, 
           "Merge Rate:", round(rate, 2), "%",
            }
    if rate >= 80:
        return {"Pull Request Merge Report",
           "----------------------------",
           "Closed PRs analyzed:": total,
           "Merged PRs:": merged, 
           "Merge Rate:", round(rate, 2), "%",
            "Status: Excellent "}
    elif rate >= 50:
        return {"Pull Request Merge Report",
           "----------------------------",
           "Closed PRs analyzed:": total,
           "Merged PRs:": merged, 
           "Merge Rate:", round(rate, 2), "%",
            "Status: Healthy "}
    elif rate >= 30:
        return {"Pull Request Merge Report",
           "----------------------------",
           "Closed PRs analyzed:": total,
           "Merged PRs:": merged, 
           "Merge Rate:", round(rate, 2), "%",
            "Status: Concerning "}
    else:
        return {"Pull Request Merge Report",
           "----------------------------",
           "Closed PRs analyzed:": total,
           "Merged PRs:": merged, 
           "Merge Rate:", round(rate, 2), "%",
            "Status: Risk "}
