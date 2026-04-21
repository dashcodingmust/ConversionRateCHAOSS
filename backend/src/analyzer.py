import asyncio
from number_of_contributions import investment
from commit_trend import commit_trend
from pr_merge_rate import pr_metrics, pr_backlog
from issue_backlog import issue_backlog
from active_maintainers import active_maintainers
from time_of_last_commit import last_commit_time
from stale_items import stale_items

KEYS = [
    "Contributor Engagement",
    "Commit Trend",
    "PR Metrics",
    "PR Backlog",
    "Issue Backlog",
    "Active Maintainers",
    "Last Commit Time",
    "Stale Items",
]

FALLBACKS = {
    "Contributor Engagement": {"conversion_rate": 0, "stage_distribution": {"D0": 0, "D1": 0, "D2": 0}},
    "Commit Trend": {"labels": [], "commit_counts": []},
    "PR Metrics": {"merge_rate": 0, "avg_merge_time_days": 0},
    "PR Backlog": {"open_prs": 0, "recently_closed_prs": 0, "backlog_ratio": 0},
    "Issue Backlog": {"open_issues": 0, "recently_closed_issues": 0, "issue_backlog_ratio": 0},
    "Active Maintainers": 0,
    "Last Commit Time": {"last_commit_date": None, "days_since_last_commit": 0},
    "Stale Items": {"stale_prs": [], "stale_issues": [], "stale_pr_count": 0, "stale_issue_count": 0},
}


async def analyze_repo(owner, repo, threshold, days=90):
    results = await asyncio.gather(
        investment(owner, repo, threshold),
        commit_trend(owner, repo, days),
        pr_metrics(owner, repo, days),
        pr_backlog(owner, repo, days),
        issue_backlog(owner, repo, days),
        active_maintainers(owner, repo, days),
        last_commit_time(owner, repo),
        stale_items(owner, repo, days),
        return_exceptions=True,
    )

    output = {}
    for key, result in zip(KEYS, results):
        if isinstance(result, Exception):
            print(f"[WARN] {key} failed: {result}")
            output[key] = FALLBACKS[key]
        else:
            output[key] = result

    return output