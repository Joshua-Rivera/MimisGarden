import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./styles.css";

const AdminPanel = React.lazy(() => import("./components/AdminPanel"));
const isAdminPage = /^\/admin\/?$/.test(window.location.pathname);

// puts the react app within the div
createRoot(document.getElementById("root")).render(
    <React.StrictMode>
        {isAdminPage ? (
            <main>
                <React.Suspense fallback={<p role="status">Loading administration…</p>}>
                    <AdminPanel />
                </React.Suspense>
            </main>
        ) : <App />}
    </React.StrictMode>
);
