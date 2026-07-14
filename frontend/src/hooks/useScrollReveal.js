import { useEffect } from "react";

export default function useScrollReveal(containerRef, refreshKey = "") {
    useEffect(() => {
        const container = containerRef.current;
        if (!container) return undefined;

        const elements = [...container.querySelectorAll(".reveal-on-scroll")];
        const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

        if (reducedMotion || !("IntersectionObserver" in window)) {
            elements.forEach((element) => element.classList.add("is-visible"));
            return undefined;
        }

        container.classList.add("reveal-enabled");
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.16, rootMargin: "0px 0px -8%" });

        elements.forEach((element) => observer.observe(element));
        return () => observer.disconnect();
    }, [containerRef, refreshKey]);
}
