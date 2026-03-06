import asyncio
from number_of_contributions import conversion_metric
from commit_trend import commit_metrics
from pr_merge_rate import pr_metrics
from issue_backlog import issue_metrics
from active_maintainers import active_maintainers

async def analyze_repo(owner, repo):
    results = await asyncio.gather(
        conversion_metric(owner, repo),
        commit_metrics(owner, repo),
        pr_metrics(owner, repo),
        issue_metrics(owner, repo),
        active_maintainers(owner, repo)
    )

    return combine(results)

def combine(results):
    return {
        "Contributor Engagement": results[0],
        "Commit Trend": results[1],
        "PR Metrics": results[2],
        "Issue Backlog": results[3],
        "Active Maintainers": results[4],
    }