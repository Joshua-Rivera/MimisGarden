import { useEffect, useRef } from "react";

export default function Hero() {
    const heroRef = useRef(null);

    useEffect(() => {
        const hero = heroRef.current;
        if (!hero) return undefined;

        let frameId;
        const updateProgress = () => {
            const distance = Math.max(hero.offsetHeight - window.innerHeight, 1);
            const progress = Math.min(Math.max(-hero.getBoundingClientRect().top / distance, 0), 1);
            hero.style.setProperty("--hero-progress", progress.toFixed(3));
            frameId = undefined;
        };
        const scheduleUpdate = () => {
            if (frameId === undefined) frameId = requestAnimationFrame(updateProgress);
        };

        updateProgress();
        window.addEventListener("scroll", scheduleUpdate, { passive: true });
        window.addEventListener("resize", scheduleUpdate);
        return () => {
            window.removeEventListener("scroll", scheduleUpdate);
            window.removeEventListener("resize", scheduleUpdate);
            if (frameId !== undefined) cancelAnimationFrame(frameId);
        };
    }, []);

    return (
        <section id="home" className="hero" ref={heroRef}>
            <div className="hero-stage">
                <div className="hero-copy">
                    <p className="small-title">Computer Vision &amp; MLOps</p>
                    <h1>Every Leaf<br />Becomes Data</h1>
                    <a href="#analyze" className="button primary-button">Analyze Plant</a>
                </div>
            </div>
        </section>
    );
}
