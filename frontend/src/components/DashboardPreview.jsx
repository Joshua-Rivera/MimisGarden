import { useRef } from "react";
import ImageUpload from "./ImageUpload";
import useScrollReveal from "../hooks/useScrollReveal";
const metrics = [
  {
    title: "Total Predictions",
    value: "1,248",
  },
  {
    title: "Average Confidence",
    value: "82%",
  },
  {
    title: "Needs Review",
    value: "23",
  },
  {
    title: "Active Model",
    value: "plant-health-v1",
  },
];

export default function DashboardPreview() {
  const dashboardRef = useRef(null);
  useScrollReveal(dashboardRef);

  const renderMetric = (metric, index) => (
    <div
      className={`metric-card metric-card-edge-${index % 2 === 0 ? "left" : "right"} reveal-on-scroll`}
      key={metric.title}
    >
      <p>{metric.title}</p>
      <h3>{metric.value}</h3>
    </div>
  );

  return (
    <section id="dashboard" className="dashboard-section" ref={dashboardRef}>
      <div className="dashboard-slide">
        <div className="section-heading reveal-on-scroll">
          <p className="small-title">Dashboard</p>
          <h2>Model insights at a glance.</h2>
          <p>
            Track predictions, confidence, review queue activity, and active model
            versions.
          </p>
        </div>

        <div className="metrics-deck">{metrics.map(renderMetric)}</div>
      </div>

      <ImageUpload />
    </section>
  );
}
