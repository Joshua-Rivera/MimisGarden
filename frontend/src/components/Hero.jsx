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
                {/* This creates the circle path where the leaves move */}
                <div className="leaf-orbit orbit-one">
                    <img src="/assets/falling-leaf.png" alt="" className="orbit-leaf" />
                </div>

                <div className="leaf-orbit orbit-two">
                    <img src="/assets/falling-leaf.png" alt="" className="orbit-leaf" />
                </div>

                <div className="leaf-orbit orbit-three">
                    <img src="/assets/falling-leaf.png" alt="" className="orbit-leaf" />
                </div>

                {/* This shows the tree image */}
                <img src="/assets/tree.png" alt="Mimi's Garden tree" className="tree-image" />
            </div>
        </section>
    );
}
