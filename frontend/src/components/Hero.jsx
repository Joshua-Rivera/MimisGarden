import cleanTree from "../assets/cleantree.png";

export default function Hero() {
    return (
        <section id="home" className="hero">
            {/*This creates the soft background behind the tree */}
            <div className="sun-circle"></div>

            {/* This creates the text on the left side */}
            <div className="hero-text">
                <p className="small-title">Computer Vision & MLOps</p>
                <h1>
                    Every Leaf
                    <br />
                    becomes data
                </h1>
                <p className="hero-description">
                    Mimi&apos;s Garden analyzes plant images, tracks confidence, logs
                    predictions, and helps improve future models through review
                </p>

                {/* These create the hero buttons */}
                <div className="hero-buttons">
                    <a href="#analyze" className="button primary-button">
                        Analyze Plant
                    </a>

                    <a href="#dashboard" className="button secondary-button">
                        View Dashboard
                    </a>
                </div>
            </div>

            {/* This creates the tree area */}
            <div className="tree-area">
                {/*
                  Falling-leaf framework:

                  1. Add a decorative container here.
                  2. Put one span inside it for every leaf you want to show.
                  3. Give the container and spans class names.
                  4. Style the leaf shape and add a falling @keyframes rule in styles.css.

                  Keep aria-hidden="true" on the container because the leaves
                  are visual decoration and should not be read by screen readers.
                */}

                {/* This shows the tree image */}
                <img src={cleanTree} alt="Mimi's Garden tree" className="tree-image" />
            </div>
        </section>
    );
}
