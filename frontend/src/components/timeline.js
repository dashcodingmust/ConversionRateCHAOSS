function TimelineItem({ title, date, description }) {
  return (
    <div className="timeline-item">
      <div className="timeline-dot"></div>
      <div className="timeline-content">
        <div className="timeline-header">
          <span className="timeline-title">{title}</span>
          <span className="timeline-date">{date}</span>
        </div>
        <div className="timeline-description">{description}</div>
      </div>
    </div>
  );
}

function Timeline({ results }) {
  return (
    <div className="section">
      <h3 className="section-title">🕒 Activity</h3>

      <div className="timeline">
        <TimelineItem
          title="Last Commit"
          date={
            results["Last Commit Time"]?.last_commit_date
              ? new Date(
                  results["Last Commit Time"].last_commit_date
                ).toLocaleString()
              : "N/A"
          }
          description={`${
            results["Last Commit Time"]?.days_since_last_commit || 0
          } days ago`}
        />

        <TimelineItem
          title="PR Activity Snapshot"
          date="Current State"
          description={`${
            results["PR Backlog"]?.open_prs || 0
          } open PRs • ${
            results["PR Backlog"]?.recently_closed_prs || 0
          } recently closed`}
        />

        <TimelineItem
          title="Issue Backlog Snapshot"
          date="Current State"
          description={`${
            results["Issue Backlog"]?.open_issues || 0
          } open issues • ${
            results["Issue Backlog"]?.recently_closed_issues || 0
          } recently closed`}
        />

        <TimelineItem
          title="Analysis Executed"
          date={new Date().toLocaleString()}
          description="Repository health metrics generated"
        />
      </div>
    </div>
  );
}

export default Timeline;