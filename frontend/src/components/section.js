function Section({ title, children }) {
  return (
    <div className="section">
      <h3 className="section-title">{title}</h3>
      {children}
    </div>
  );
}

export default Section;