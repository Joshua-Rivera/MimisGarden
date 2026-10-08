import { useEffect, useRef, useState } from "react";
import ImageUpload from "./ImageUpload";
import useScrollReveal from "../hooks/useScrollReveal";
import { getCurrentModel } from "../lib/api";
export default function DashboardPreview() {
  const dashboardRef = useRef(null);
  const [model, setModel] = useState(null); const [error, setError] = useState("");
  useScrollReveal(dashboardRef);
  useEffect(() => {
    let active = true;
    getCurrentModel().then(value => { if (active) setModel(value); }).catch(() => { if (active) setError("Analysis is unavailable until the trained model is ready."); });
    return () => { active = false; };
  }, []);
  const metrics = [
    { title: "Active model", value: model?.model_version || "Unavailable" },
    { title: "Supported conditions", value: "3" },
    { title: "Validation accuracy", value: model?.accuracy == null ? "Not available" : `${(model.accuracy * 100).toFixed(1)}%` },
    { title: "Validation F1", value: model?.f1_score == null ? "Not available" : model.f1_score.toFixed(3) },
  ];
  return <section id="dashboard" className="dashboard-section" ref={dashboardRef}>
    <div className="dashboard-slide"><div className="section-heading reveal-on-scroll"><p className="small-title">Model insights</p><h2>Know what the model can tell you.</h2><p>Healthy, leaf spots, or severe damage. Validation scores describe the training dataset; performance on your plants may differ.</p></div>
    <div className="metrics-deck">{metrics.map((metric, index) => <div className={`metric-card metric-card-edge-${index % 2 === 0 ? "left" : "right"} reveal-on-scroll`} key={metric.title}><p>{metric.title}</p><h3>{metric.value}</h3></div>)}</div>
    {error && <p role="status">{error}</p>}</div><ImageUpload />
  </section>;
}
