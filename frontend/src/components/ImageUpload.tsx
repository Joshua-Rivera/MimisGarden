import {
  useEffect,
  useRef,
  useState,
  type ChangeEvent,
  type DragEvent,
} from "react";
import PredictionCard, { type Prediction } from "./PredictionCard";
import useScrollReveal from "../hooks/useScrollReveal";

const analysisWords = [
  "Watering",
  "Taking root",
  "Reading leaves",
  "Growing insight",
  "Checking for wilting",
];

const acceptedImageTypes = new Set(["image/png", "image/jpeg", "image/webp"]);

export default function ImageUpload() {
  const uploadRef = useRef<HTMLElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [prediction, setPrediction] = useState<Prediction | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [fileError, setFileError] = useState("");
  const [analysisWordIndex, setAnalysisWordIndex] = useState(0);
  useScrollReveal(uploadRef, prediction?.prediction_id ?? "");

  useEffect(() => {
    if (!selectedFile) {
      setPreviewUrl("");
      return undefined;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setPreviewUrl(objectUrl);
    return () => URL.revokeObjectURL(objectUrl);
  }, [selectedFile]);

  useEffect(() => {
    if (!isAnalyzing) return undefined;

    const wordTimer = window.setInterval(() => {
      setAnalysisWordIndex((current) => (current + 1) % analysisWords.length);
    }, 720);

    const resultTimer = window.setTimeout(() => {
      setPrediction({
        prediction_id: "pred_fake_001",
        plant_state: "dry_wilting",
        possible_condition: "possible_water_stress",
        confidence: 0.82,
        severity: "medium",
        suggestion:
          "Check soil moisture. If the soil is dry, water the plant and monitor it over the next few days.",
        model_version: "plant-health-v0-fake",
        needs_review: false,
      });
      setIsAnalyzing(false);
    }, 3600);

    return () => {
      window.clearInterval(wordTimer);
      window.clearTimeout(resultTimer);
    };
  }, [isAnalyzing]);

  function selectFile(file: File) {
    if (!acceptedImageTypes.has(file.type)) {
      setFileError("Choose a PNG, JPG, or WebP image.");
      return;
    }

    setSelectedFile(file);
    setPrediction(null);
    setIsAnalyzing(false);
    setFileError("");
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) selectFile(file);
    event.target.value = "";
  }

  function handleDragOver(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    if (event.dataTransfer.types.includes("Files")) setIsDragging(true);
  }

  function handleDragLeave(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
      setIsDragging(false);
    }
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    setIsDragging(false);
    const file = event.dataTransfer.files[0];
    if (file) selectFile(file);
  }

  function handleAnalyzeClick() {
    if (!selectedFile || isAnalyzing) return;

    setPrediction(null);
    setAnalysisWordIndex(0);
    setIsAnalyzing(true);
  }

  return (
    <section id="analyze" className="image-upload-section" ref={uploadRef}>
      <div className="analyze-workspace reveal-on-scroll">
        <div className="analyze-heading">
          <p className="small-title">Analyze</p>
          <h2>Upload a plant image.</h2>
          <p>Choose a clear plant or leaf photo to test the prediction workflow.</p>
        </div>

        <label
          className={`file-drop-zone${isDragging ? " is-dragging" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
        >
          <span className="file-drop-icon" aria-hidden="true">+</span>
          <span>{isDragging ? "Drop your plant image" : "Choose or drop an image"}</span>
          <small>PNG, JPG or WebP</small>
          <input
            type="file"
            accept="image/png, image/jpeg, image/webp"
            onChange={handleFileChange}
          />
        </label>

        {fileError && <p className="file-error" role="alert">{fileError}</p>}

        {previewUrl && (
          <div className="image-preview-box">
            <img src={previewUrl} alt="Selected plant preview" />
            <p className="selected-file-name">{selectedFile?.name}</p>
          </div>
        )}

        <button
          className="button primary-button analyze-button"
          type="button"
          onClick={handleAnalyzeClick}
          disabled={!selectedFile || isAnalyzing}
        >
          {isAnalyzing ? "Analyzing…" : "Analyze plant"}
        </button>

        <div className="analysis-output" aria-live="polite">
          {isAnalyzing ? (
            <div className="analysis-loader" role="status">
              <div className="analysis-loader-ring" aria-hidden="true">
                <span className="analysis-loader-sprout">●</span>
              </div>
              <p className="analysis-loader-word" key={analysisWords[analysisWordIndex]}>
                {analysisWords[analysisWordIndex]}
              </p>
            </div>
          ) : prediction ? (
            <div className="results-panel">
              <PredictionCard prediction={prediction} />
              <div className="result-board">
                <p className="small-title">Next steps</p>
                <h4>Analysis complete</h4>
                <p>Review the care guidance and monitor the plant over the next few days.</p>
                <a className="button secondary-button" href="#dashboard">
                  View model insights
                </a>
              </div>
            </div>
          ) : (
            <div className="prediction-placeholder">
              <p className="small-title">Prediction</p>
              <h3>No prediction yet</h3>
              <p>Upload an image and select Analyze plant to see results.</p>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}
