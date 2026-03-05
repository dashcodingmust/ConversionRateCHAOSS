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

  const healthScore = results
    ? Math.round(
        ((results["PR Merge Rate"] || 0) +
          Math.min(results["Active Maintainers"] || 0, 50) * 2 +
          Math.min(results["Commit Trend"]?.recent_commits || 0, 100)) /
          3,
      )
    : 0;

  return (
    <div className="app">
      {/* SIDEBAR */}

      <div className="sidebar">
        <h2> Configuration</h2>

        <label>Repository Owner</label>
        <input value={owner} onChange={(e) => setOwner(e.target.value)} />

        <label>Repository Name</label>
        <input value={repo} onChange={(e) => setRepo(e.target.value)} />

        <label>Contributor Threshold</label>

        <input
          type="range"
          min="1"
          max="50"
          value={threshold}
          onChange={(e) => setThreshold(e.target.value)}
        />

        <div className="threshold">Threshold: {threshold}</div>

        <button className="run-btn" onClick={analyzeRepo}>
          🚀 Run Analysis
        </button>

        <div className="help-box">
          <b>How to use</b>
          <ol>
            <li>Enter repository owner</li>
            <li>Enter repository name</li>
            <li>Adjust contributor threshold</li>
            <li>Click Run Analysis</li>
          </ol>
        </div>
      </div>

      {/* MAIN */}

      <div className="main">
        <h1 className="title">GitHub Project Health Dashboard</h1>

        <p className="subtitle">
          Analyze repository activity, contributors, and project sustainability
        </p>

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            Fetching repository data...
          </div>
        )}

        {results && (
          <>
            {/* METRICS */}

            <div className="metrics">
              <Card title="Health Score" value={healthScore} icon="💚" />
              <Card
                title="Active Maintainers"
                value={results["Active Maintainers"]}
                icon="👨‍💻"
              />
              <Card
                title="PR Merge Rate"
                value={results["PR Merge Rate"]}
                icon="🔀"
              />
              <Card
                title="Open Issues"
                value={results["Issue Backlog"]?.open_issues}
                icon="🐞"
              />
            </div>

            {/* CHARTS */}

            <div className="chart-grid">
              <Chart title="Commit Trend">
                <Line
                  data={{
                    labels: ["Previous", "Recent"],
                    datasets: [
                      {
                        label: "Commits",
                        data: [
                          results["Commit Trend"]?.previous_commits || 0,
                          results["Commit Trend"]?.recent_commits || 0,
                        ],
                        borderColor: "#22c55e",
                        backgroundColor: "#22c55e",
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                  }}
                />
              </Chart>

              <Chart title="Issue Backlog">
                <Bar
                  data={{
                    labels: ["Open Issues"],
                    datasets: [
                      {
                        label: "Issues",
                        data: [results["Issue Backlog"]?.open_issues || 0],
                        backgroundColor: "#ef4444",
                      },
                    ],
                  }}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                  }}
                />
              </Chart>

              <Chart title="Maintainer Capacity">
                <Doughnut
                  data={{
                    labels: ["Maintainers", "Remaining"],
                    datasets: [
                      {
                        data: [
                          results["Active Maintainers"],
                          50 - results["Active Maintainers"],
                        ],
                        backgroundColor: ["#3b82f6", "#1e293b"],
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
                          results["PR Merge Rate"],
                          100 - results["PR Merge Rate"],
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
