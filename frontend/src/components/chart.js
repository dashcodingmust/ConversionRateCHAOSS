function ChartWrapper({ title, children }) {
  return (
    <div className="card chart">
      <h3>{title}</h3>
      <div className="chart-container">{children}</div>
    </div>
  );
}

export default ChartWrapper;