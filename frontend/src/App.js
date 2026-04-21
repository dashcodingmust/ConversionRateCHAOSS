import React, { useState, useEffect, useRef, useCallback } from "react";
import axios from "axios";
import Card from "./components/card";
import { calculateHealthScore } from "./utils/health";
import RepoHeader from "./components/repo";
import Section from "./components/section";
import ChartWrapper from "./components/chart";
import Timeline from "./components/timeline";
import CompareView from "./components/compare";
import "./App.css";

import {
  Chart as ChartJS,
  BarElement, LineElement, ArcElement, PointElement,
  CategoryScale, LinearScale, Tooltip, Legend,
} from "chart.js";
import { Line, Doughnut } from "react-chartjs-2";

ChartJS.register(BarElement, LineElement, ArcElement, PointElement, CategoryScale, LinearScale, Tooltip, Legend);

const TIME_WINDOWS = [
  { label: "30d", value: 30 },
  { label: "60d", value: 60 },
  { label: "90d", value: 90 },
  { label: "180d", value: 180 },
];

// ─── Token Status Banner ──────────────────────────────────────────────────────

function TokenBanner({ keyInfo, onSwitch }) {
  const [open, setOpen] = useState(false);
  const [switching, setSwitching] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    const handler = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", handler);
    return () => document.removeEventListener("mousedown", handler);
  }, []);

  if (!keyInfo) return null;

  const { authenticated, active, keys } = keyInfo;

  const handleSwitch = async (name) => {
    if (name === active) { setOpen(false); return; }
    setSwitching(true);
    try {
      await axios.post("http://127.0.0.1:8000/keys/active", { name });
      onSwitch(name);
    } catch (e) {
      console.error("Failed to switch key", e);
    }
    setSwitching(false);
    setOpen(false);
  };

  return (
    <div className="token-banner-wrapper" ref={ref}>
      <button
        className={`token-banner ${authenticated ? "token-ok" : "token-warn"}`}
        onClick={() => keys.length > 1 && setOpen(!open)}
        style={{ cursor: keys.length > 1 ? "pointer" : "default" }}
        title={keys.length > 1 ? "Click to switch API key" : undefined}
      >
        <span className="token-dot" />
        <span className="token-text">
          {authenticated
            ? <>✓ <strong>{active}</strong>'s key active</>
            : "⚠ No API key — rate limited"}
        </span>
        {keys.length > 1 && (
          <span className="token-chevron">{open ? "▲" : "▼"}</span>
        )}
      </button>

      {open && keys.length > 1 && (
        <div className="token-dropdown">
          <div className="token-dropdown-label">Switch API key</div>
          {keys.map((name) => (
            <button
              key={name}
              className={`token-dropdown-item ${name === active ? "token-dropdown-active" : ""}`}
              onClick={() => handleSwitch(name)}
              disabled={switching}
            >
              {name === active && <span className="token-active-dot" />}
              {name}
              {name === active && <span className="token-current-badge">current</span>}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Repo Autocomplete ────────────────────────────────────────────────────────

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
      if (owner === fetchedOwner) return;
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
    <div className="autocomplete-wrapper" ref={wrapperRef}>
      <div className="autocomplete-input-row">
        <input
          value={value}
          onChange={(e) => { onChange(e.target.value); setOpen(true); }}
          onFocus={() => setOpen(true)}
          placeholder={
            loading ? "Loading repos…" :
            repos.length > 0 ? `${repos.length} repos found` :
            owner.length >= 2 ? "e.g. react" : "Enter owner first"
          }
          disabled={!owner || owner.trim().length < 2}
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

// ─── Funnel Chart ─────────────────────────────────────────────────────────────

function FunnelChart({ d0, d1, d2 }) {
  const total = d0 + d1 + d2 || 1;
  const stages = [
    { label: "D0", sublabel: "First-timers (≤20)", count: d0, color: "#ef4444" },
    { label: "D1", sublabel: "Occasional", count: d1, color: "#f59e0b" },
    { label: "D2", sublabel: "Regular", count: d2, color: "#22c55e" },
  ];
  const maxCount = Math.max(d0, 1);
  const widths = [d0, d1, d2].map((v) => Math.max((v / maxCount) * 100, 6));
  const d0ToD1Rate = d0 > 0 ? Math.round(((d1 + d2) / d0) * 100) : 0;
  const d1ToD2Rate = d1 > 0 ? Math.round((d2 / d1) * 100) : 0;

  return (
    <div className="funnel-wrapper">
      {stages.map((s, i) => (
        <React.Fragment key={s.label}>
          <div className="funnel-stage">
            <div className="funnel-label-left">
              <span className="funnel-stage-name">{s.label}</span>
              <span className="funnel-stage-sub">{s.sublabel}</span>
            </div>
            <div className="funnel-bar-area">
              <div className="funnel-bar" style={{ width: `${widths[i]}%`, background: s.color }} />
            </div>
            <div className="funnel-label-right">
              <span className="funnel-count">{s.count}</span>
              <span className="funnel-pct">{Math.round((s.count / total) * 100)}%</span>
            </div>
          </div>
          {i === 0 && (
            <div className="funnel-conversion-row">
              <span className="funnel-conv-label">{d0ToD1Rate}% advance to D1+</span>
              <span className="funnel-conv-arrow">↓</span>
            </div>
          )}
          {i === 1 && (
            <div className="funnel-conversion-row">
              <span className="funnel-conv-label">{d1ToD2Rate}% advance to D2</span>
              <span className="funnel-conv-arrow">↓</span>
            </div>
          )}
        </React.Fragment>
      ))}
    </div>
  );
}

// ─── Stale Items ──────────────────────────────────────────────────────────────

function StaleList({ items, type }) {
  const [expanded, setExpanded] = useState(false);
  const visible = expanded ? items : items.slice(0, 3);
  const icon = type === "pr" ? "🔀" : "🐛";
  if (items.length === 0) return <p className="stale-empty">No stale {type === "pr" ? "PRs" : "issues"} — all clear ✅</p>;
  return (
    <div className="stale-list">
      {visible.map((item) => (
        <a key={item.number} href={item.url} target="_blank" rel="noreferrer" className="stale-item">
          <span className="stale-icon">{icon}</span>
          <span className="stale-meta">
            <span className="stale-title">#{item.number} {item.title}</span>
            <span className="stale-author">@{item.author}</span>
          </span>
          <span className="stale-days">{item.days_stale}d</span>
        </a>
      ))}
      {items.length > 3 && (
        <button className="stale-toggle" onClick={() => setExpanded(!expanded)}>
          {expanded ? "Show less ↑" : `+${items.length - 3} more`}
        </button>
      )}
    </div>
  );
}

// ─── App ──────────────────────────────────────────────────────────────────────

function App() {
  const [activeTab, setActiveTab] = useState("dashboard");
  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [threshold, setThreshold] = useState(50);
  const [days, setDays] = useState(90);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [keyInfo, setKeyInfo] = useState(null);

  // Load key info on mount
  useEffect(() => {
    axios.get("http://127.0.0.1:8000/keys")
      .then((res) => setKeyInfo(res.data))
      .catch(() => setKeyInfo(null));
  }, []);

  const handleKeySwitched = (name) => {
    setKeyInfo((prev) => prev ? { ...prev, active: name } : prev);
  };

  const analyzeRepo = async () => {
    if (!owner.trim() || !repo.trim()) { setError("Please enter both a repository owner and name."); return; }
    setLoading(true); setError(null); setResults(null);
    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        owner: owner.trim(), repo: repo.trim(), threshold, days,
      });
      setResults(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || err?.message || "Failed to reach the backend. Is the server running?");
    }
    setLoading(false);
  };

  const healthScore = calculateHealthScore(results);
  const latestWeeklyCommits = results?.["Commit Trend"]?.commit_counts?.slice(-1)[0] || 0;
  const conversionRate = results?.["Contributor Engagement"]?.conversion_rate || 0;
  const stageDistribution = results?.["Contributor Engagement"]?.stage_distribution || { D0: 0, D1: 0, D2: 0 };
  const staleData = results?.["Stale Items"];
  const repoMeta = results?.["Repo Meta"];

  return (
    <div className="app">
      <div className="sidebar">
        <h2>Configuration</h2>

        {/* Token / Key Status */}
        <TokenBanner keyInfo={keyInfo} onSwitch={handleKeySwitched} />

        <label style={{ marginTop: "20px", display: "block" }}>Repository Owner</label>
        <input value={owner} onChange={(e) => { setOwner(e.target.value); setRepo(""); }} placeholder="e.g. facebook" />

        <label>Repository Name</label>
        <RepoAutocomplete owner={owner} value={repo} onChange={setRepo} />

        <label>Contributor Threshold (D2)</label>
        <input type="range" min="21" max="150" step="1" value={threshold} onChange={(e) => setThreshold(Number(e.target.value))} />
        <div className="threshold">Threshold: {threshold} contributions</div>

        <label>Time Window</label>
        <div className="time-window-group">
          {TIME_WINDOWS.map((w) => (
            <button key={w.value} className={`time-btn ${days === w.value ? "active" : ""}`} onClick={() => setDays(w.value)}>
              {w.label}
            </button>
          ))}
        </div>

        <button className="run-btn" onClick={analyzeRepo} disabled={loading}>
          {loading ? "Analyzing…" : "🚀 Run Analysis"}
        </button>
      </div>

      <div className="main">
        <h1 className="title">GitHub Project Health Dashboard</h1>

        <div className="nav-tabs">
          <button className={`nav-tab ${activeTab === "dashboard" ? "active" : ""}`} onClick={() => setActiveTab("dashboard")}>
            📊 Dashboard
          </button>
          <button className={`nav-tab ${activeTab === "compare" ? "active" : ""}`} onClick={() => setActiveTab("compare")}>
            ⚖️ Compare
          </button>
        </div>

        {activeTab === "compare" && <CompareView />}

        {activeTab === "dashboard" && (<>
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              Fetching repository data…
            </div>
          )}
          {error && (
            <div className="error-banner">
              <span className="error-icon">⚠️</span>
              <span>{error}</span>
            </div>
          )}
          {!results && !loading && !error && (
            <div className="empty-state">
              <div className="empty-icon">🔭</div>
              <p className="empty-title">No repo analyzed yet</p>
              <p className="empty-sub">Enter an owner and pick a repo from the dropdown to get started.</p>
              <div className="empty-examples">
                Try: <span>torvalds / linux</span> · <span>facebook / react</span> · <span>microsoft / vscode</span>
              </div>
            </div>
          )}
          {results && (
            <>
              <RepoHeader owner={owner} repo={repo} healthScore={healthScore} meta={repoMeta} />

              <Section title="🟢 Contribution Health">
                <div className="metrics">
                  <Card title="Health Score" value={healthScore} icon="💚" />
                  <Card title="PR Merge Rate (%)" value={results["PR Metrics"]?.merge_rate || 0} icon="🔀" />
                  <Card title="Avg Merge Time (days)" value={results["PR Metrics"]?.avg_merge_time_days || 0} icon="⏱️" />
                  <Card title="Latest Weekly Commits" value={latestWeeklyCommits} icon="📊" />
                </div>
              </Section>

              <Section title="🟡 Backlog Pressure">
                <div className="metrics">
                  <Card title="Open PRs" value={results["PR Backlog"]?.open_prs || 0} icon="📂" />
                  <Card title="Recently Closed PRs" value={results["PR Backlog"]?.recently_closed_prs || 0} icon="✅" />
                  <Card title="PR Backlog Ratio" value={results["PR Backlog"]?.backlog_ratio || 0} icon="⚖️" />
                  <Card title="Open Issues" value={results["Issue Backlog"]?.open_issues || 0} icon="🐞" />
                  <Card title="Recently Closed Issues" value={results["Issue Backlog"]?.recently_closed_issues || 0} icon="📦" />
                  <Card title="Issue Backlog Ratio" value={results["Issue Backlog"]?.issue_backlog_ratio || 0} icon="📊" />
                </div>
              </Section>

              <Section title="🔵 Activity Signals">
                <div className="metrics">
                  <Card title="Active Maintainers" value={results["Active Maintainers"] || 0} icon="👨‍💻" />
                  <Card title="Last Commit Date"
                    value={results["Last Commit Time"]?.last_commit_date
                      ? new Date(results["Last Commit Time"].last_commit_date).toLocaleDateString()
                      : "N/A"}
                    icon="🗓️"
                  />
                  <Card title="Days Since Last Commit" value={results["Last Commit Time"]?.days_since_last_commit || 0} icon="⏳" />
                </div>
              </Section>

              {staleData && (
                <Section title="🔴 Stale Items (no activity 30+ days)">
                  <div className="metrics">
                    <Card title="Stale PRs" value={staleData.stale_pr_count} icon="🕸️" />
                    <Card title="Stale Issues" value={staleData.stale_issue_count} icon="🕸️" />
                  </div>
                  <div className="stale-grid">
                    <div className="stale-column">
                      <h4 className="stale-col-title">Stale Pull Requests</h4>
                      <StaleList items={staleData.stale_prs} type="pr" />
                    </div>
                    <div className="stale-column">
                      <h4 className="stale-col-title">Stale Issues</h4>
                      <StaleList items={staleData.stale_issues} type="issue" />
                    </div>
                  </div>
                </Section>
              )}

              <div className="section-divider"></div>

              <div className="chart-grid">
                <ChartWrapper title="Weekly Commit Trend">
                  <Line
                    data={{
                      labels: results["Commit Trend"]?.labels || [],
                      datasets: [{ label: "Weekly Commits", data: results["Commit Trend"]?.commit_counts || [], borderColor: "#22c55e", backgroundColor: "rgba(34,197,94,0.2)", tension: 0.3, fill: true }],
                    }}
                    options={{ responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } }}
                  />
                </ChartWrapper>

                <ChartWrapper title="Conversion Rate Gauge">
                  <div className="gauge-wrapper">
                    <div className="gauge-inner">
                      <Doughnut
                        data={{
                          labels: ["Converted", "Remaining"],
                          datasets: [{ data: [conversionRate, 100 - conversionRate], backgroundColor: ["#22c55e", "#1e293b"], borderWidth: 0 }],
                        }}
                        options={{ rotation: -90, circumference: 180, cutout: "70%", plugins: { legend: { display: false }, tooltip: { enabled: false } } }}
                      />
                      <div className="gauge-value">{conversionRate}%</div>
                    </div>
                  </div>
                </ChartWrapper>

                <ChartWrapper title="Contributor Funnel (D0 → D1 → D2)">
                  <FunnelChart d0={stageDistribution.D0} d1={stageDistribution.D1} d2={stageDistribution.D2} />
                </ChartWrapper>

                <ChartWrapper title="Merge Rate">
                  <Doughnut
                    data={{
                      labels: ["Merged", "Rejected"],
                      datasets: [{ data: [results["PR Metrics"]?.merge_rate || 0, 100 - (results["PR Metrics"]?.merge_rate || 0)], backgroundColor: ["#22c55e", "#ef4444"] }],
                    }}
                    options={{ responsive: true, maintainAspectRatio: false }}
                  />
                </ChartWrapper>
              </div>

              <Timeline results={results} />
            </>
          )}
        </>)}
      </div>
    </div>
  );
}

export default App;
