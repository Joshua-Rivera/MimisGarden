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
        <section id="dashboard" className="dashboard-selection">
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

            {/* This creates upload box preview*/}
            <div id="analyze" className="upload-preview">
                <h3>Analyze a Plant Image</h3>
                <p>Upload a plant or leaf image to begin the prediction process.</p>
                <button> Upload Plant Image </button>
                </div>    
        </section>
    )

}