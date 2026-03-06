import React, { useState } from "react";
import axios from "axios";
import "./App.css";

import {
  Chart as ChartJS,
  BarElement,
  LineElement,
  ArcElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from "chart.js";

import { Bar, Line, Doughnut } from "react-chartjs-2";

ChartJS.register(
  BarElement,
  LineElement,
  ArcElement,
  PointElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
);

function App() {
  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [threshold, setThreshold] = useState(20);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeRepo = async () => {
    setLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:8000/analyze", {
        owner,
        repo,
        threshold,
      });

      setResults(response.data);
    } catch {
      alert("API Error");
    }

    setLoading(false);
  };

  const mergeRate = results?.["PR Metrics"]?.merge_rate || 0;
  const avgMergeTime = results?.["PR Metrics"]?.avg_merge_time_days || 0;
  const backlogRatio = results?.["PR Backlog"]?.backlog_ratio || 0;
  const activeMaintainers = results?.["Active Maintainers"] || 0;
  const latestWeeklyCommits =
    results?.["Commit Trend"]?.commit_counts?.slice(-1)[0] || 0;

  const speedScore = Math.max(0, 100 - avgMergeTime * 10);
  const backlogScore = Math.max(0, 100 - backlogRatio * 30);
  const maintainerScore = Math.min(activeMaintainers * 5, 100);
  const commitScore = Math.min(latestWeeklyCommits * 2, 100);

  const healthScore = Math.round(
    mergeRate * 0.25 +
      speedScore * 0.15 +
      backlogScore * 0.2 +
      maintainerScore * 0.2 +
      commitScore * 0.2,
  );

  const conversionRate =
    results?.["Contributor Engagement"]?.conversion_rate || 0;

  const stageDistribution = results?.["Contributor Engagement"]
    ?.stage_distribution || {
    D0: 0,
    D1: 0,
    D2: 0,
  };

  return (
    <div className="app">
      <div className="sidebar">
        <h2>Configuration</h2>

        <label>Repository Owner</label>
        <input value={owner} onChange={(e) => setOwner(e.target.value)} />

        <label>Repository Name</label>
        <input value={repo} onChange={(e) => setRepo(e.target.value)} />

        <label>Contributor Threshold</label>
        <input
          type="range"
          min="1"
          max="100"
          step="1"
          value={threshold}
          onChange={(e) => setThreshold(Number(e.target.value))}
        />

        <div className="threshold">Threshold: {threshold}</div>

        <button className="run-btn" onClick={analyzeRepo}>
          🚀 Run Analysis
        </button>
      </div>

      <div className="main">
        <h1 className="title">GitHub Project Health Dashboard</h1>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            Fetching repository data...
          </div>
        )}

        {results && (
          <>
            <div className="metrics">
              <Card title="Health Score" value={healthScore} icon="💚" />
              <Card
                title="Active Maintainers"
                value={results["Active Maintainers"] || 0}
                icon="👨‍💻"
              />
              <Card
                title="PR Merge Rate (%)"
                value={results["PR Metrics"]?.merge_rate || 0}
                icon="🔀"
              />

              <Card
                title="Avg Merge Time (days)"
                value={results["PR Metrics"]?.avg_merge_time_days || 0}
                icon="⏱️"
              />

              <Card
                title="Open PRs"
                value={results["PR Backlog"]?.open_prs || 0}
                icon="📂"
              />

              <Card
                title="Recently Closed PRs"
                value={results["PR Backlog"]?.recently_closed_prs || 0}
                icon="✅"
              />

              <Card
                title="Backlog Ratio"
                value={results["PR Backlog"]?.backlog_ratio || 0}
                icon="⚖️"
              />
              <Card
                title="Open Issues"
                value={results["Issue Backlog"]?.open_issues || 0}
                icon="🐞"
              />

              <Card
                title="Recently Closed Issues"
                value={results["Issue Backlog"]?.recently_closed_issues || 0}
                icon="📦"
              />

              <Card
                title="Issue Backlog Ratio"
                value={results["Issue Backlog"]?.issue_backlog_ratio || 0}
                icon="⚖️"
              />

              <Card
                title="Last Commit Date"
                value={
                  results["Last Commit Time"]?.last_commit_date
                    ? new Date(
                        results["Last Commit Time"].last_commit_date,
                      ).toLocaleDateString()
                    : "N/A"
                }
                icon="🗓️"
              />

              <Card
                title="Days Since Last Commit"
                value={results["Last Commit Time"]?.days_since_last_commit || 0}
                icon="⏳"
              />
            </div>

            <div className="chart-grid">
              <Chart title="Weekly Commit Trend">
                <Line
                  data={{
                    labels: results["Commit Trend"]?.labels || [],
                    datasets: [
                      {
                        label: "Weekly Commits",
                        data: results["Commit Trend"]?.commit_counts || [],
                        borderColor: "#22c55e",
                        backgroundColor: "rgba(34,197,94,0.2)",
                        tension: 0.3,
                        fill: true,
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                      y: { beginAtZero: true },
                    },
                  }}
                />
              </Chart>

              <Chart title="Conversion Rate Gauge">
                <div className="gauge-wrapper">
                  <div className="gauge-inner">
                    <Doughnut
                      data={{
                        labels: ["Converted", "Remaining"],
                        datasets: [
                          {
                            data: [conversionRate, 100 - conversionRate],
                            backgroundColor: ["#22c55e", "#1e293b"],
                            borderWidth: 0,
                          },
                        ],
                      }}
                      options={{
                        rotation: -90,
                        circumference: 180,
                        cutout: "70%",
                        plugins: {
                          legend: { display: false },
                          tooltip: { enabled: false },
                        },
                      }}
                    />
                    <div className="gauge-value">{conversionRate}%</div>
                  </div>
                </div>
              </Chart>

              <Chart title="Contributor Stage Distribution">
                <Doughnut
                  data={{
                    labels: [
                      "D0 (One-time)",
                      "D1 (Occasional)",
                      "D2 (Regular)",
                    ],
                    datasets: [
                      {
                        data: [
                          stageDistribution.D0,
                          stageDistribution.D1,
                          stageDistribution.D2,
                        ],
                        backgroundColor: ["#ef4444", "#f59e0b", "#22c55e"],
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                  }}
                />
              </Chart>

              <Chart title="Merge Rate">
                <Doughnut
                  data={{
                    labels: ["Merged", "Rejected"],
                    datasets: [
                      {
                        data: [
                          results["PR Metrics"]?.merge_rate || 0,
                          100 - (results["PR Metrics"]?.merge_rate || 0),
                        ],
                        backgroundColor: ["#22c55e", "#ef4444"],
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                  }}
                />
              </Chart>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

function Card({ title, value, icon }) {
  return (
    <div className="card metric-card">
      <div className="metric-header">
        <span className="icon">{icon}</span>
        <span className="metric-title">{title}</span>
      </div>
      <div className="metric-value">{value}</div>
    </div>
  );
}

function Chart({ title, children }) {
  return (
    <div className="card chart">
      <h3>{title}</h3>
      <div className="chart-container">{children}</div>
    </div>
  );
}

export default App;
