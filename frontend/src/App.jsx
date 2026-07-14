import { useRef, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import IntroLaptopScene from "./components/IntroLaptopScene.jsx";
import GardenBackground from "./components/GardenBackground.jsx";
import Hero from "./components/Hero.jsx";
import DashboardPreview from "./components/DashboardPreview.jsx";

export default function App() {
    const gardenRef = useRef(null);
    const [introReady, setIntroReady] = useState(() => (
        typeof window !== "undefined"
        && window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ));
    const [gardenReady, setGardenReady] = useState(() => (
        typeof window !== "undefined"
        && window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ));

    return (

        <>
        <Navbar isVisible={introReady} /> {/* shows after the laptop zoom */}

        <IntroLaptopScene
            gardenRef={gardenRef}
            onIntroReadyChange={setIntroReady}
            onGardenReadyChange={setGardenReady}
        />

        <GardenBackground ref={gardenRef} isActive={gardenReady} />

        <Hero /> {/* shows the hero component */}

        <DashboardPreview /> {/* shows the dashboard preview component */}
        </>

    );
}
