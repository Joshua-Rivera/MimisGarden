export default function Navbar({ isVisible = true }) {

    return(
        <nav
            className={`navbar ${isVisible ? "navbar-visible" : "navbar-hidden"}`}
            aria-hidden={!isVisible}
            inert={isVisible ? undefined : ""}
        >
            {/* Navbar content goes here, specifically logo area */}
            <div className="brand">
                <span className="brand-icon">ADD LOGO</span>
                <span>Mimi&apos;s Garden</span>
            </div>

            {/* Navigation links */}
            <div className="nav-links">
                <a href="#home">Home</a>
                <a href="#analyze">Analyze</a>
                <a href="#reviews">Reviews</a>
                <a href="#models">Models</a>
            </div>
        </nav>
    );

}
