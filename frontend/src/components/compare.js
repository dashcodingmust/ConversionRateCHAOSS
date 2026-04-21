import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { calculateHealthScore, getHealthStatus } from "../utils/health";

// ─── Shared Autocomplete ──────────────────────────────────────────────────────

function RepoAutocomplete({ owner, value, onChange }) {
  const [repos, setRepos] = useState([]);
  const [filtered, setFiltered] = useState([]);
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [fetchedOwner, setFetchedOwner] = useState("");
  const wrapperRef = useRef(null);

  useEffect(() => {
    if (!owner || owner.trim().length < 2) { setRepos([]); setFiltered([]); return; }
    const timer = setTimeout(async () => {
      if (owner.trim() === fetchedOwner) return;
      setLoading(true);
      try {
        const res = await axios.get(`http://127.0.0.1:8000/repos/${owner.trim()}`);
        setRepos(res.data);
        setFetchedOwner(owner.trim());
      } catch { setRepos([]); } finally { setLoading(false); }
    }, 600);
    return () => clearTimeout(timer);
  }, [owner]);

  useEffect(() => {
    if (!value) setFiltered(repos.slice(0, 8));
    else setFiltered(repos.filter((r) => r.name.toLowerCase().includes(value.toLowerCase())).slice(0, 8));
  }, [value, repos]);

  useEffect(() => {
    const handler = (e) => { if (wrapperRef.current && !wrapperRef.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  return (
    <div className="autocomplete-wrapper" ref={wrapperRef} style={{ margin: "4px 0 0 0" }}>
      <div className="autocomplete-input-row">
        <input
          value={value}
          onChange={(e) => { onChange(e.target.value); setOpen(true); }}
          onFocus={() => setOpen(true)}
          placeholder={loading ? "Loading repos…" : repos.length > 0 ? `${repos.length} repos found` : owner.length >= 2 ? "e.g. react" : "Enter owner first"}
          disabled={!owner || owner.trim().length < 2}
          style={{ width: "100%", padding: "10px 12px", borderRadius: "8px", border: "1px solid #1e293b", background: "#020617", color: "white", fontSize: "13px", boxSizing: "border-box" }}
        />
        {loading && <span className="autocomplete-spinner" />}
      </div>
      {open && filtered.length > 0 && (
        <ul className="autocomplete-dropdown">
          {filtered.map((r) => (
            <li key={r.name} className="autocomplete-item" onMouseDown={() => { onChange(r.name); setOpen(false); }}>
              <span className="ac-name">{r.name}</span>
              <span className="ac-meta">
                {r.language && <span className="ac-lang">{r.language}</span>}
                {r.stars > 0 && <span className="ac-stars">⭐ {r.stars.toLocaleString()}</span>}
              </span>
              {r.description && <span className="ac-desc">{r.description}</span>}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// ─── Compare Metric Row ───────────────────────────────────────────────────────

function CompareMetric({ label, left, right, higherIsBetter = true }) {
  const leftNum = parseFloat(left) || 0;
  const rightNum = parseFloat(right) || 0;
  const leftWins = higherIsBetter ? leftNum >= rightNum : leftNum <= rightNum;
  const tied = leftNum === rightNum;
  return (
    <div className="compare-row">
      <div className={`compare-cell ${!tied && leftWins ? "compare-winner" : ""}`}>{left}</div>
      <div className="compare-label">{label}</div>
      <div className={`compare-cell ${!tied && !leftWins ? "compare-winner" : ""}`}>{right}</div>
    </div>
  );
}

// ─── Single Panel ─────────────────────────────────────────────────────────────

function ComparePanel({ side, onResult }) {
  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const analyze = async () => {
    if (!owner.trim() || !repo.trim()) { setError("Enter both owner and repo."); return; }
    setLoading(true); setError(null);
    try {
      const res = await axios.post("http://127.0.0.1:8000/analyze", { owner: owner.trim(), repo: repo.trim(), threshold: 50, days: 90 });
      onResult({ owner: owner.trim(), repo: repo.trim(), data: res.data });
    } catch (err) { setError(err?.response?.data?.detail || err?.message || "Failed to fetch."); }
    setLoading(false);
  };

  return (
    <div className="compare-panel">
      <h3 className="compare-panel-title">Repo {side}</h3>
      <label>Owner</label>
      <input value={owner} onChange={(e) => { setOwner(e.target.value); setRepo(""); }} placeholder="e.g. facebook"
        style={{ width: "100%", padding: "10px 12px", borderRadius: "8px", border: "1px solid #1e293b", background: "#020617", color: "white", fontSize: "13px", boxSizing: "border-box", marginTop: "4px" }} />
      <label style={{ marginTop: "10px", display: "block" }}>Repository</label>
      <RepoAutocomplete owner={owner} value={repo} onChange={setRepo} />
      <button className="run-btn" onClick={analyze} disabled={loading} style={{ marginTop: "12px" }}>
        {loading ? "Analyzing…" : "🔍 Analyze"}
      </button>
      {error && <p className="compare-error">{error}</p>}
    </div>
  );
}

// ─── Compare View ─────────────────────────────────────────────────────────────

function CompareView() {
  const [left, setLeft] = useState(null);
  const [right, setRight] = useState(null);
  const leftScore = calculateHealthScore(left?.data);
  const rightScore = calculateHealthScore(right?.data);
  const leftStatus = getHealthStatus(leftScore);
  const rightStatus = getHealthStatus(rightScore);

  return (
    <div className="compare-view">
      <h2 className="compare-heading">⚖️ Repository Comparison</h2>
      <p className="compare-subheading">Analyze two repos side-by-side to compare their health metrics.</p>
      <div className="compare-inputs">
        <ComparePanel side="A" onResult={setLeft} />
        <div className="compare-vs">VS</div>
        <ComparePanel side="B" onResult={setRight} />
      </div>
      {left && right && (
        <div className="compare-results">
          <div className="compare-header-row">
            <div className="compare-repo-label">
              <div className="compare-repo-name">{left.owner}/{left.repo}</div>
              <span className={`health-badge ${leftStatus.class}`}>{leftStatus.label}</span>
            </div>
            <div className="compare-header-center">Metric</div>
            <div className="compare-repo-label compare-repo-label-right">
              <div className="compare-repo-name">{right.owner}/{right.repo}</div>
              <span className={`health-badge ${rightStatus.class}`}>{rightStatus.label}</span>
            </div>
          </div>
          <CompareMetric label="Health Score" left={leftScore} right={rightScore} />
          <CompareMetric label="PR Merge Rate (%)" left={left.data["PR Metrics"]?.merge_rate || 0} right={right.data["PR Metrics"]?.merge_rate || 0} />
          <CompareMetric label="Avg Merge Time (days)" left={left.data["PR Metrics"]?.avg_merge_time_days || 0} right={right.data["PR Metrics"]?.avg_merge_time_days || 0} higherIsBetter={false} />
          <CompareMetric label="Open PRs" left={left.data["PR Backlog"]?.open_prs || 0} right={right.data["PR Backlog"]?.open_prs || 0} higherIsBetter={false} />
          <CompareMetric label="PR Backlog Ratio" left={left.data["PR Backlog"]?.backlog_ratio || 0} right={right.data["PR Backlog"]?.backlog_ratio || 0} higherIsBetter={false} />
          <CompareMetric label="Open Issues" left={left.data["Issue Backlog"]?.open_issues || 0} right={right.data["Issue Backlog"]?.open_issues || 0} higherIsBetter={false} />
          <CompareMetric label="Issue Backlog Ratio" left={left.data["Issue Backlog"]?.issue_backlog_ratio || 0} right={right.data["Issue Backlog"]?.issue_backlog_ratio || 0} higherIsBetter={false} />
          <CompareMetric label="Active Maintainers" left={left.data["Active Maintainers"] || 0} right={right.data["Active Maintainers"] || 0} />
          <CompareMetric label="Days Since Last Commit" left={left.data["Last Commit Time"]?.days_since_last_commit || 0} right={right.data["Last Commit Time"]?.days_since_last_commit || 0} higherIsBetter={false} />
          <CompareMetric label="Stale PRs" left={left.data["Stale Items"]?.stale_pr_count || 0} right={right.data["Stale Items"]?.stale_pr_count || 0} higherIsBetter={false} />
          <CompareMetric label="Stale Issues" left={left.data["Stale Items"]?.stale_issue_count || 0} right={right.data["Stale Items"]?.stale_issue_count || 0} higherIsBetter={false} />
          <CompareMetric label="Conversion Rate (%)" left={left.data["Contributor Engagement"]?.conversion_rate || 0} right={right.data["Contributor Engagement"]?.conversion_rate || 0} />
        </div>
      )}
    </div>
  );
}

export default CompareView;
