export default function Navbar({ isVisible = true }) {
  return (
    <nav
      className={`navbar ${isVisible ? "navbar-visible" : "navbar-hidden"}`}
      aria-label="Primary navigation"
      aria-hidden={!isVisible}
      inert={isVisible ? undefined : ""}
    >
      <a className="brand" href="#home" aria-label="Mimi's Garden home">
        <span className="brand-icon" aria-hidden="true">🌿</span>
        <span>Mimi&apos;s Garden</span>
      </a>

      <div className="nav-links">
        <a href="#home">Home</a>
        <a href="#dashboard">Insights</a>
        <a className="nav-action" href="#analyze">Analyze</a>
      </div>
    </nav>
  );
}
