import requests

def backlog_status(issue_count):
    if issue_count <= 20:
        return "Healthy "
    elif issue_count <= 100:
        return "Moderate "
    elif issue_count <= 500:
        return "High "
    else:
        return "Critical "


def issue_backlog(owner, repo):

    url = f"https://api.github.com/repos/{owner}/{repo}"
    response = requests.get(url)
    data = response.json()

    open_issues = data["open_issues_count"]

    print("\n Issue Backlog Report")
    print("------------------------")
    print("Open Issues:", open_issues)
    print("Backlog Status:", backlog_status(open_issues))