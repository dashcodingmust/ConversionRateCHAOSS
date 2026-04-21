import { getHealthStatus } from "../utils/health";

function RepoHeader({ owner, repo, healthScore, meta }) {
  const status = getHealthStatus(healthScore);

  return (
    <div className="repo-header">
      <div className="repo-info">
        <div className="repo-name-row">
          <h2 className="repo-name">
            {meta?.full_name || (owner && repo ? `${owner}/${repo}` : "Repository Overview")}
          </h2>
          {meta?.url && (
            <a href={meta.url} target="_blank" rel="noreferrer" className="repo-link">
              ↗
            </a>
          )}
        </div>

        {meta?.description && (
          <p className="repo-description">{meta.description}</p>
        )}

        <div className="repo-meta">
          {meta && (
            <>
              <span>⭐ {meta.stars.toLocaleString()}</span>
              <span>🍴 {meta.forks.toLocaleString()}</span>
              <span>🐞 {meta.open_issues.toLocaleString()} open issues</span>
              {meta.language && <span>🔵 {meta.language}</span>}
              <span className="repo-meta-divider">·</span>
            </>
          )}
          <span>Updated: {new Date().toLocaleTimeString()}</span>
          <span className={`health-badge ${status.class}`}>{status.label}</span>
        </div>
      </div>

      <div className="repo-health-score">
        <div className="score-number">{healthScore}</div>
        <div className="score-label">Health Score</div>
      </div>
    </div>
  );
}

export default RepoHeader;
