// backend URL
const API_BASE_URL = "http://127.0.0.1:8000";
// main API path
const API_V1 = `${API_BASE_URL}/api/v1`;
// sends an image to the backend for processing
export async function createPrediction(file: File) {
  //  creates form that can hold an image file
  const formData = new FormData();

  //  adds the selected image to the form
  formData.append("file", file);

  //  sends the image to the backend FstAPI
  const response = await fetch(`${API_V1}/predict`, {
    method: "POST",
    body: formData,
  });

  // checks if the backend failed :(
  if (!response.ok) {
    throw new Error("Prediction failed");
  }

  // returns the prediction result
  return response.json();
}

//  gets the dashboard summary numbers
export async function getSummaryMetrics() {
  const response = await fetch(`${API_V1}/metrics/summary`);

  if (!response.ok) {
    throw new Error("Could not load summary metrics");
  }

  return response.json();
}

//  gets the current active model
export async function getCurrentModel() {
  const response = await fetch(`${API_V1}/models/current`);

  if (!response.ok) {
    throw new Error("Could not load current model");
  }

  return response.json();
}

//  gets the prediction history
export async function getPredictions() {
  const response = await fetch(`${API_V1}/predictions`);

  if (!response.ok) {
    throw new Error("Could not load predictions");
  }

  return response.json();
}

//  gets confidence statistics
export async function getConfidenceMetrics() {
  const response = await fetch(`${API_V1}/metrics/confidence`);

  if (!response.ok) {
    throw new Error("Could not load confidence metrics");
  }

  return response.json();
}
