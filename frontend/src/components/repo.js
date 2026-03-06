import { getHealthStatus } from "../utils/health";

function RepoHeader({ owner, repo, healthScore }) {
  const status = getHealthStatus(healthScore);

  return (
    <div className="repo-header">
      <div className="repo-info">
        <h2 className="repo-name">
          {owner && repo ? `${owner}/${repo}` : "Repository Overview"}
        </h2>

        <div className="repo-meta">
          <span>
            Last Updated: {new Date().toLocaleTimeString()}
          </span>

          <span className={`health-badge ${status.class}`}>
            {status.label}
          </span>
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