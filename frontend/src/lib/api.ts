// This is the backend URL
const API_BASE_URL = "http://127.0.0.1:8000";

// This sends an image to the backend for prediction
export async function createPrediction(file: File) {
  // This creates a form that can hold an image file
  const formData = new FormData();

  // This adds the selected image to the form
  formData.append("file", file);

  // This sends the image to the backend
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    body: formData,
  });

  // This checks if the backend failed
  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  // This gives back the prediction result
  return response.json();
}

// This gets the dashboard summary numbers
export async function getSummaryMetrics() {
  const response = await fetch(`${API_BASE_URL}/metrics/summary`);

  if (!response.ok) {
    throw new Error("Could not load summary metrics");
  }

  return response.json();
}

// This gets the current active model
export async function getCurrentModel() {
  const response = await fetch(`${API_BASE_URL}/models/current`);

  if (!response.ok) {
    throw new Error("Could not load current model");
  }

  return response.json();
}

// This gets the prediction history
export async function getPredictions() {
  const response = await fetch(`${API_BASE_URL}/predictions`);

  if (!response.ok) {
    throw new Error("Could not load predictions");
  }

  return response.json();
}
