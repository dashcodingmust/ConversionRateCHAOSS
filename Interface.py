from backend.src.number_of_contributions import investment
from backend.src.time_of_last_commit import last_commit_time
from backend.src.issue_backlog import issue_backlog
from backend.src.pr_merge_rate import pr_merge_rate
from backend.src.commit_trend import commit_trend
from backend.src.active_maintainers import active_maintainers


def analyze_repo(owner, repo, threshold):
    results = {}

    results["Contributor Engagement"] = investment(owner, repo ,threshold)
    results["Last Commit Activity"] = last_commit_time(1, owner, repo)
    results["Commit Trend"] = commit_trend(owner, repo)
    results["Active Maintainers"] = active_maintainers(owner, repo)
    results["Issue Backlog"] = issue_backlog(owner, repo)
    results["PR Merge Rate"] = pr_merge_rate(owner, repo)

    return results