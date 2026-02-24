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

    print("\n Pull Request Merge Report")
    print("----------------------------")
    print("Closed PRs analyzed:", total)
    print("Merged PRs:", merged)
    print("Merge Rate:", round(rate, 2), "%")

    if rate >= 80:
        print("Status: Excellent ")
    elif rate >= 50:
        print("Status: Healthy ")
    elif rate >= 30:
        print("Status: Concerning ")
    else:
        print("Status: Risk 🚨")