import { useEffect, useRef } from "react";
import laptopImage from "../assets/laptop.png";

const clamp = (value) => Math.min(Math.max(value, 0), 1);

export default function IntroLaptopScene({
    gardenRef,
    onIntroReadyChange = () => {},
    onGardenReadyChange = () => {},
}) {
    const introRef = useRef(null);
    const screenAnchorRef = useRef(null);
    const readyStateRef = useRef(null);
    const gardenReadyStateRef = useRef(null);

    useEffect(() => {
        const intro = introRef.current;
        if (!intro) return undefined;

        const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
        const previousScrollRestoration = window.history.scrollRestoration;
        let frameId;

        if (!window.location.hash) {
            window.history.scrollRestoration = "manual";
            window.scrollTo(0, 0);
        }

        // Only notify App when the navbar visibility actually changes.
        const publishReadyState = (isReady) => {
            if (readyStateRef.current === isReady) return;
            readyStateRef.current = isReady;
            onIntroReadyChange(isReady);
        };

        const publishGardenReadyState = (isReady) => {
            if (gardenReadyStateRef.current === isReady) return;
            gardenReadyStateRef.current = isReady;
            onGardenReadyChange(isReady);
        };

        const updateIntro = () => {
            if (reducedMotion.matches) {
                publishReadyState(true);
                publishGardenReadyState(true);
                const garden = gardenRef?.current;
                if (garden) {
                    garden.style.setProperty("--garden-left", "0px");
                    garden.style.setProperty("--garden-top", "0px");
                    garden.style.setProperty("--garden-width", `${window.innerWidth}px`);
                    garden.style.setProperty("--garden-height", `${window.innerHeight}px`);
                    garden.style.setProperty("--garden-left-slope", "0%");
                    garden.style.setProperty("--garden-right-slope", "0%");
                    garden.style.setProperty("--garden-radius", "0px");
                    garden.style.setProperty("--garden-tree-width", `${Math.min(Math.max(window.innerWidth * 0.43, 390), 640)}px`);
                    garden.style.zIndex = "0";
                }
                frameId = undefined;
                return;
            }

            // Convert this section's scroll position into a value from 0 to 1.
            const scrollDistance = Math.max(intro.offsetHeight - window.innerHeight, 1);
            const scrolledDistance = -intro.getBoundingClientRect().top;
            const progress = clamp(scrolledDistance / scrollDistance);
            const slideProgress = clamp(
                (scrolledDistance - scrollDistance) / Math.max(window.innerHeight, 1),
            );
            const zoomProgress = clamp((progress - 0.08) / 0.72);
            const easedZoom = 1 - Math.pow(1 - zoomProgress, 3);
            const photoFade = clamp((progress - 0.62) / 0.25);
            const screenMorph = clamp((progress - 0.92) / 0.075);

            // Landscape screens use a true cover calculation. Portrait screens
            // show more of the laptop so the bezel remains readable.
            const isPortraitLayout = window.innerWidth / window.innerHeight < 0.82;
            const coverScale = Math.max(
                window.innerWidth / 2048,
                window.innerHeight / 1356,
            );
            const photoWidth = isPortraitLayout
                ? window.innerWidth * 1.5
                : 2048 * coverScale;
            const photoTop = isPortraitLayout
                ? window.innerHeight * 0.52
                : window.innerHeight * 0.5;
            const screenWidth = photoWidth * 0.571;
            const screenHeight = photoWidth * (1356 / 2048) * 0.428;

            // Calculate enough scale for the laptop screen to cover any viewport shape.
            const targetScale = Math.max(
                window.innerWidth / Math.max(screenWidth, 1),
                window.innerHeight / Math.max(screenHeight, 1),
            );
            const currentScale = 1 + (targetScale - 1) * easedZoom;
            const screenLeftInset = 5.6 * (1 - screenMorph);
            const screenRightInset = 7.3 * (1 - screenMorph);
            const baseRadius = Math.min(Math.max(screenWidth * 0.025, 8), 18);
            const contentRadius = baseRadius * (1 - screenMorph);

            intro.style.setProperty("--intro-progress", progress.toFixed(3));
            intro.style.setProperty("--intro-slide", slideProgress.toFixed(3));
            intro.style.setProperty("--intro-zoom", easedZoom.toFixed(3));
            intro.style.setProperty("--intro-lift", `${(easedZoom * 5).toFixed(2)}vh`);
            intro.style.setProperty("--intro-scale", currentScale.toFixed(3));
            intro.style.setProperty("--intro-photo-width", `${photoWidth.toFixed(1)}px`);
            intro.style.setProperty("--intro-photo-top", `${photoTop.toFixed(1)}px`);
            intro.style.setProperty("--intro-photo-fade", photoFade.toFixed(3));
            intro.style.setProperty("--intro-handoff", screenMorph.toFixed(3));
            intro.style.setProperty("--intro-frame-opacity", (0.35 * (1 - screenMorph)).toFixed(3));
            intro.style.setProperty("--intro-screen-left-inset", `${screenLeftInset.toFixed(2)}%`);
            intro.style.setProperty("--intro-screen-right-inset", `${screenRightInset.toFixed(2)}%`);
            intro.style.setProperty("--intro-screen-radius", `${contentRadius.toFixed(2)}px`);

            const garden = gardenRef?.current;
            const screenAnchor = screenAnchorRef.current;
            if (garden && screenAnchor) {
                const screenRect = screenAnchor.getBoundingClientRect();
                const sceneLeft = screenRect.left * (1 - screenMorph);
                const sceneTop = screenRect.top * (1 - screenMorph);
                const sceneWidth = screenRect.width + (window.innerWidth - screenRect.width) * screenMorph;
                const sceneHeight = screenRect.height + (window.innerHeight - screenRect.height) * screenMorph;
                const finalTreeWidth = Math.min(Math.max(window.innerWidth * 0.43, 390), 640);
                const treeWidth = sceneWidth * 0.36 + (finalTreeWidth - sceneWidth * 0.36) * screenMorph;

                garden.style.setProperty("--garden-left", `${sceneLeft.toFixed(2)}px`);
                garden.style.setProperty("--garden-top", `${sceneTop.toFixed(2)}px`);
                garden.style.setProperty("--garden-width", `${sceneWidth.toFixed(2)}px`);
                garden.style.setProperty("--garden-height", `${sceneHeight.toFixed(2)}px`);
                garden.style.setProperty("--garden-left-slope", `${screenLeftInset.toFixed(2)}%`);
                garden.style.setProperty("--garden-right-slope", `${screenRightInset.toFixed(2)}%`);
                garden.style.setProperty("--garden-radius", `${contentRadius.toFixed(2)}px`);
                garden.style.setProperty("--garden-tree-width", `${treeWidth.toFixed(2)}px`);
                garden.style.zIndex = screenMorph >= 1 ? "0" : "5";
            }

            publishReadyState(slideProgress >= 0.08);
            publishGardenReadyState(slideProgress >= 0.98);
            frameId = undefined;
        };

        // Scroll and resize events only schedule one visual update per frame.
        const scheduleUpdate = () => {
            if (frameId === undefined) frameId = requestAnimationFrame(updateIntro);
        };

        updateIntro();
        window.addEventListener("scroll", scheduleUpdate, { passive: true });
        window.addEventListener("resize", scheduleUpdate);
        reducedMotion.addEventListener("change", scheduleUpdate);

        return () => {
            window.removeEventListener("scroll", scheduleUpdate);
            window.removeEventListener("resize", scheduleUpdate);
            reducedMotion.removeEventListener("change", scheduleUpdate);
            window.history.scrollRestoration = previousScrollRestoration;
            if (frameId !== undefined) cancelAnimationFrame(frameId);
        };
    }, [gardenRef, onGardenReadyChange, onIntroReadyChange]);

    return (
        <section className="intro-laptop-scene" ref={introRef} aria-hidden="true">
            <div className="intro-laptop-stage">
                <img className="intro-laptop-backdrop" src={laptopImage} alt="" />

                {/* The photo and screen share one wrapper so they zoom together. */}
                <div className="intro-laptop-frame">
                    <img className="intro-laptop-photo" src={laptopImage} alt="" />

                    {/* This invisible anchor keeps the shared garden aligned to the glass. */}
                    <div className="intro-laptop-screen" ref={screenAnchorRef} />
                </div>
            </div>
        </section>
    );
}
