import { useEffect, useState } from "react";
import { getPredictions, getReviews, getReviewImage, getSummaryMetrics, submitReview } from "../lib/api";
import type { Prediction } from "./PredictionCard";
const readable = (s: string) => s.replace(/_/g, " ");
function ReviewItem({ prediction: p, token, onSaved }: { prediction: Prediction; token: string; onSaved: () => void }) {
  const [image, setImage] = useState("");
  const [label, setLabel] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);
  useEffect(() => {
    const controller = new AbortController(); let url = "";
    getReviewImage(p.prediction_id, token, controller.signal).then(blob => {
      if (!controller.signal.aborted) { url = URL.createObjectURL(blob); setImage(url); }
    }).catch(() => { if (!controller.signal.aborted) setError("Image unavailable. Inspect the image before approving."); });
    return () => { controller.abort(); if (url) URL.revokeObjectURL(url); };
  }, [p.prediction_id, token]);
  return <form className="review-item" onSubmit={async event => {
    event.preventDefault(); setSaving(true); setError("");
    try { await submitReview(p.prediction_id, label, notes, token); onSaved(); }
    catch (err) { setError(err instanceof Error ? err.message : "Could not save review"); }
    finally { setSaving(false); }
  }}>
    {image && <img src={image} alt="Plant awaiting review" />}
    <p>Predicted: {readable(p.plant_state)} · {(p.confidence * 100).toFixed(1)}%</p>
    <label>Correct condition<select required value={label} onChange={e => setLabel(e.target.value)}><option value="" disabled>Choose after inspecting</option><option value="uncertain">Unsupported or unclear image</option><option value="healthy">Healthy</option><option value="leaf_spots">Leaf spots</option><option value="severe_damage">Severe damage</option></select></label>
    <label>Review notes<textarea maxLength={2000} value={notes} onChange={e => setNotes(e.target.value)} /></label>
    <button className="button primary-button" disabled={saving || !image || !label}>{saving ? "Saving…" : "Save correction"}</button>
    {error && <p role="alert">{error}</p>}
  </form>;
}
export default function AdminPanel() {
  const [input, setInput] = useState(""); const [token, setToken] = useState("");
  const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  const [summary, setSummary] = useState<{total_predictions: number; average_confidence: number; needs_review_count: number} | null>(null);
  const [predictions, setPredictions] = useState<Prediction[]>([]); const [reviews, setReviews] = useState<Prediction[]>([]);
  const [offset, setOffset] = useState(0);
  const [selected, setSelected] = useState<Prediction | null>(null);
  async function refresh(key = token, page = offset) {
    setBusy(true); setError("");
    try {
      const [metrics, history, queue] = await Promise.all([getSummaryMetrics(key), getPredictions(key, page), getReviews(key)]);
      setSummary(metrics); setPredictions(history); setReviews(queue); setToken(key); setInput(""); setOffset(page);
    } catch (err) { setError(err instanceof Error ? err.message : "Could not load administration"); }
    finally { setBusy(false); }
  }
  return <section id="manage" className="admin-panel">
    <p className="small-title">Administration</p><h2>History and human review</h2>
    <p>For the garden administrator. Your token is held only in this page’s memory.</p>
    {!token ? <form onSubmit={e => { e.preventDefault(); void refresh(input, 0); }}><label>Administrator token<input type="password" autoComplete="off" required value={input} onChange={e => setInput(e.target.value)} /></label><button className="button primary-button" disabled={busy}>{busy ? "Connecting…" : "Open administration"}</button></form> : <>
      <div className="admin-actions"><button disabled={busy} onClick={() => void refresh()}>Refresh</button><button disabled={busy} onClick={() => { setToken(""); setSummary(null); setPredictions([]); setReviews([]); setSelected(null); setError(""); }}>Sign out</button></div>
      {summary && <p>{summary.total_predictions} predictions · {(summary.average_confidence * 100).toFixed(1)}% average confidence · {summary.needs_review_count} awaiting review</p>}
      <h3>Prediction history</h3>
      {!predictions.length ? <p>No predictions on this page.</p> : <div className="history-scroll"><table><thead><tr><th>Prediction</th><th>Condition</th><th>Confidence</th><th>Model</th><th>Action</th></tr></thead><tbody>{predictions.map(p => <tr key={p.prediction_id}><td>{p.prediction_id}</td><td>{readable(p.plant_state)}</td><td>{(p.confidence * 100).toFixed(1)}%</td><td>{p.model_version}</td><td><button onClick={() => setSelected(p)}>Review image</button></td></tr>)}</tbody></table></div>}
      <div className="admin-actions"><button disabled={busy || offset === 0} onClick={() => void refresh(token, Math.max(0, offset - 50))}>Previous</button><button disabled={busy || predictions.length < 50} onClick={() => void refresh(token, offset + 50)}>Next</button></div>
      {selected && <div><h3>Review selected prediction</h3><button onClick={() => setSelected(null)}>Close review</button><ReviewItem key={selected.prediction_id} prediction={selected} token={token} onSaved={() => { setSelected(null); void refresh(); }} /></div>}
      <h3>Review queue</h3><p>Up to 100 pending images. Saved corrections leave this queue.</p>
      {!reviews.length ? <p>No images need review.</p> : <div className="review-grid">{reviews.map(p => <ReviewItem key={p.prediction_id} prediction={p} token={token} onSaved={() => void refresh()} />)}</div>}
    </>}{error && <p role="alert">{error}</p>}
  </section>;
}
