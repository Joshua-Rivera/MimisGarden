import AdminPanel from "./components/AdminPanel";
import { useRef, useState } from "react";
import Navbar from "./components/Navbar.jsx";
import IntroLaptopScene from "./components/IntroLaptopScene.jsx";
import GardenBackground from "./components/GardenBackground.jsx";
import Hero from "./components/Hero.jsx";
import DashboardPreview from "./components/DashboardPreview.jsx";
import LimitationsSection from "./components/LimitationsSection.jsx";
import useIsPhone from "./hooks/useIsPhone.js";
export default function App() {
  const gardenRef = useRef(null);
  const isPhone = useIsPhone();
  const prefersReducedMotion = () =>
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const [introReady, setIntroReady] = useState(() => isPhone || prefersReducedMotion());
  const [gardenReady, setGardenReady] = useState(() => isPhone || prefersReducedMotion());

  return (
    <div className={isPhone ? "app phone-layout" : "app"}>
      <Navbar isVisible={isPhone || introReady} />
      {!isPhone && (
        <IntroLaptopScene
          gardenRef={gardenRef}
          onIntroReadyChange={setIntroReady}
          onGardenReadyChange={setGardenReady}
        />
      )}
      <GardenBackground ref={gardenRef} isActive={isPhone || gardenReady} />
      <Hero />
      <DashboardPreview />
      <AdminPanel />
      <LimitationsSection />
    </div>
  );
}
