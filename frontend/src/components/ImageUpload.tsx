import { useEffect, useRef, useState, type ChangeEvent } from "react";
import PredictionCard, { type Prediction } from "./PredictionCard";
import useScrollReveal from "../hooks/useScrollReveal";

const analysisWords = [
    "Wilting away",
    "Watering",
    "Taking root",
    "Reading leaves",
    "Growing insight",
];

export default function ImageUpload() {
    const uploadRef = useRef<HTMLElement>(null);
    // stores image file the user selects
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    //stores image preview link
    const [previewUrl, setPreviewUrl] = useState("");

    //stores prediction result
    const [prediction, setPrediction] = useState<Prediction | null>(null);
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [analysisWordIndex, setAnalysisWordIndex] = useState(0);
    useScrollReveal(uploadRef, prediction?.prediction_id ?? "");

    useEffect(() => {
        if (!isAnalyzing) return undefined;

        const wordTimer = window.setInterval(() => {
            setAnalysisWordIndex((current) => (current + 1) % analysisWords.length);
        }, 620);

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
        }, 3200);

        return () => {
            window.clearInterval(wordTimer);
            window.clearTimeout(resultTimer);
        };
    }, [isAnalyzing]);

    //runs when user chooses an image
    function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0];

        if (!file){return;}

        //saves selected file
        setSelectedFile(file);

        //creates preview of selected img
        setPreviewUrl(URL.createObjectURL(file));

        //clears old prediction when new img is chosen
        setPrediction(null);
        setIsAnalyzing(false);
    }

    //analyze button activate
    function handleAnalyzeClick() {
        if (!selectedFile){return;}

        setPrediction(null);
        setAnalysisWordIndex(0);
        setIsAnalyzing(true);
    }
    return (
    <section id="analyze" className="image-upload-section" ref={uploadRef}>
      {/* This creates the upload box */}
      <div className="upload-panel reveal-on-scroll">
        <p className="small-title">Analyze</p>

        <h2>Upload a plant image.</h2>

        <p>
          Choose a plant or leaf photo to test the prediction workflow.
        </p>

        {/* This creates the file picker */}
        <input
          type="file"
          accept="image/png, image/jpeg, image/jpg, image/webp"
          onChange={handleFileChange}
        />

        {/* This shows the image preview after the user chooses a file */}
        {previewUrl && (
          <div className="image-preview-box">
            <img src={previewUrl} alt="Selected plant preview" />
          </div>
        )}

        {/* This creates the analyze button */}
        <button onClick={handleAnalyzeClick} disabled={isAnalyzing}>
          {isAnalyzing ? "Analyzing..." : "Analyze Plant"}
        </button>

        {isAnalyzing && (
          <div className="analysis-loader" role="status" aria-live="polite">
            <div className="analysis-loader-ring" aria-hidden="true">
              <span className="analysis-loader-sprout">●</span>
            </div>
            <p className="analysis-loader-word" key={analysisWords[analysisWordIndex]}>
              {analysisWords[analysisWordIndex]}
            </p>
          </div>
        )}
      </div>

      {/* This shows the prediction after Analyze is clicked */}
      <PredictionCard prediction={prediction} />
    </section>
  );
}
