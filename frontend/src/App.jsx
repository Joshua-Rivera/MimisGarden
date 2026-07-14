import { useRef, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import IntroLaptopScene from "./components/IntroLaptopScene.jsx";
import GardenBackground from "./components/GardenBackground.jsx";
import Hero from "./components/Hero.jsx";
import DashboardPreview from "./components/DashboardPreview.jsx";

export default function App() {
  const gardenRef = useRef(null);
  const prefersReducedMotion = () =>
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const [introReady, setIntroReady] = useState(prefersReducedMotion);
  const [gardenReady, setGardenReady] = useState(prefersReducedMotion);

  return (
    <>
      <Navbar isVisible={introReady} />
      <IntroLaptopScene
        gardenRef={gardenRef}
        onIntroReadyChange={setIntroReady}
        onGardenReadyChange={setGardenReady}
      />
      <GardenBackground ref={gardenRef} isActive={gardenReady} />
      <Hero />
      <DashboardPreview />
    </>
  );
}
