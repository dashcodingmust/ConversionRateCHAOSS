from backend.src.Number_of_contributions import investment
from backend.src.time_of_last_commit import lastCommitTime
from backend.src.issue_backlog import issue_backlog
from backend.src.PR_merge_rate import pr_merge_rate
from backend.src.Commit_trend_decline import commit_trend
from backend.src.Active_maintainers import active_maintainers


def analyze_repo(owner, repo):
    results = {}

    results["Contributor Engagement"] = investment(owner, repo)
    results["Last Commit Activity"] = lastCommitTime(1, owner, repo)
    results["Commit Trend"] = commit_trend(owner, repo)
    results["Active Maintainers"] = active_maintainers(owner, repo)
    results["Issue Backlog"] = issue_backlog(owner, repo)
    results["PR Merge Rate"] = pr_merge_rate(owner, repo)

    return results