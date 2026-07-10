import Navbar from "./components/Navbar.jsx";
import Hero from "./components/Hero.jsx";
import DashboardPreview from "./components/DashboardPreview.jsx";

export default function App() {
    return (

        <>
        <Navbar /> {/* shows the navbar component */}

        <Hero /> {/* shows the hero component */}

        <DashboardPreview /> {/* shows the dashboard preview component */}
        </>

    );
}