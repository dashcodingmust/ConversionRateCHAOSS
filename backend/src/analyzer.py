import asyncio
from number_of_contributions import investment
from commit_trend import commit_trend
from pr_merge_rate import pr_metrics, pr_backlog
from issue_backlog import issue_backlog
from active_maintainers import active_maintainers
from time_of_last_commit import last_commit_time

async def analyze_repo(owner, repo, threshold):
    results = await asyncio.gather(
        investment(owner, repo, threshold),
        commit_trend(owner, repo),
        pr_metrics(owner, repo),
        pr_backlog(owner, repo),
        issue_backlog(owner, repo),
        active_maintainers(owner, repo),
        last_commit_time(owner, repo)
    )

    return combine(results)

def combine(results):
    return {
        "Contributor Engagement": results[0],
        "Commit Trend": results[1],
        "PR Metrics": results[2],
        "PR Backlog": results[3],
        "Issue Backlog": results[4],
        "Active Maintainers": results[5],
        "Last Commit Time": results[6]
    }