import monsterraleaf from "../assets/monterraleaf.png";

export default function Navbar({ isVisible = true }) {
  return (
    <nav
      className={`navbar ${isVisible ? "navbar-visible" : "navbar-hidden"}`}
      aria-label="Primary navigation"
      aria-hidden={!isVisible}
      inert={isVisible ? undefined : ""}
    >
      <a className="brand" href="#home" aria-label="Mimi's Garden home">
    <div className="brand-icon">
          <img className="brand-icon" src={monsterraleaf} alt="brand-icon" />
        </div>
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
