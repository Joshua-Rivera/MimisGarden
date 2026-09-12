const configuredBase = (import.meta.env.VITE_API_BASE_URL || (import.meta.env.DEV ? "http://127.0.0.1:8000" : "https://mimisgarden-production.up.railway.app")).trim();
// Hosting settings may supply a hostname without a scheme. Preserve same-origin paths.
const origin = configuredBase.startsWith("/") || /^https?:\/\//i.test(configuredBase)
  ? configuredBase
  : `https://${configuredBase}`;
const BASE = origin.replace(/\/+$/, "") + "/api/v1";
export async function apiRequest(path: string, options: RequestInit = {}, token = "") {
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(BASE + path, { ...options, headers, signal: options.signal ?? AbortSignal.timeout(60000) });
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(typeof body?.detail === "string" ? body.detail : `Request failed (${response.status})`);
  }
  return response.json();
}
export function createPrediction(file: File) {
  const body = new FormData(); body.append("file", file);
  return apiRequest("/predict", { method: "POST", body });
}
export const getSummaryMetrics = (token = "") => apiRequest("/metrics/summary", {}, token);
export const getCurrentModel = () => apiRequest("/models/current");
export const getPredictions = (token = "", offset = 0) => apiRequest(`/predictions?offset=${offset}&limit=50`, {}, token);
export const getConfidenceMetrics = (token = "") => apiRequest("/metrics/confidence", {}, token);
export const getReviews = (token: string) => apiRequest("/reviews", {}, token);
export const submitReview = (id: string, label: string, notes: string, token: string) => apiRequest(`/reviews/${encodeURIComponent(id)}`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ correct_label: label, review_notes: notes }) }, token);
export async function getReviewImage(id: string, token: string, signal: AbortSignal) {
  const response = await fetch(`${BASE}/reviews/${encodeURIComponent(id)}/image`, { headers: { Authorization: `Bearer ${token}` }, signal });
  if (!response.ok) throw new Error("Image unavailable");
  return response.blob();
}
