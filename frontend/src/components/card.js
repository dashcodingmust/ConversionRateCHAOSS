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
  export default Card;