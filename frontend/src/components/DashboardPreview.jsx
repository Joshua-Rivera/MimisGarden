import ImageUpload from "./ImageUpload";
const metrics = [
  {
    title: "Total Predictions",
    value: "1,248 (placeholder)",
  },
  {
    title: "Average Confidence",
    value: "82% (placeholder)",
  },
  {
    title: "Needs Review",
    value: "23 (placeholder)",
  },
  {
    title: "Active Model",
    value: "plant-health-v1",
  },
];


export default function DashboardPreview() {

    return (
        <section id="dashboard" className="dashboard-section">
            {/*This creates the dashbaord title*/}
            <div className="section-heading">
                <p className="small-title">Dashboard</p>
                <h2>Model Insights at a glance.</h2>
                <p>
                    Track predictions, confidence, review queue activity, and active model
                    versions.
                </p>
            </div>
            {/*This creates dashbaord row of cards*/}
            <div className="metrics-grid">
            {metrics.map((metric) => (
                <div className="metric-card" key={metric.title}>
                <p>{metric.title}</p>
                <h3>{metric.value}</h3>
                </div>
            ))}
            </div>

            {/* This creates the image upload and prediction area */}
            <ImageUpload />
        </section>
    )

}
