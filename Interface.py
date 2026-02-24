from backend.src.Number_of_contributions import investment
from backend.src.time_of_last_commit import lastCommitTime
from backend.src.issue_backlog import issue_backlog
from backend.src.PR_merge_rate import pr_merge_rate
from backend.src.Commit_trend_decline import commit_trend
from backend.src.Active_maintainers import active_maintainers


def main():

    print("====================================")
    print("   GitHub Project Health Analyzer   ")
    print("====================================\n")

    owner = input("Enter repository owner: ")
    repo = input("Enter repository name: ")

    print("\nRunning analysis...\n")

    print("🔹 Contributor Engagement")
    investment(owner, repo)

    print("\n🔹 Last Commit Activity")
    lastCommitTime(1, owner, repo)

    print("\n🔹 Commit Trend")
    commit_trend(owner, repo)

    print("\n🔹 Active Maintainers")
    active_maintainers(owner, repo)

    print("\n🔹 Issue Backlog")
    issue_backlog(owner, repo)

    print("\n🔹 PR Merge Rate")
    pr_merge_rate(owner, repo)

    print("\n====================================")
    print("        Analysis Complete ✅        ")
    print("====================================")


if __name__ == "__main__":
    main()