import { useRef, useState, type ChangeEvent } from "react";
import PredictionCard, { type Prediction } from "./PredictionCard";
import useScrollReveal from "../hooks/useScrollReveal";

export default function ImageUpload() {
    const uploadRef = useRef<HTMLElement>(null);
    // stores image file the user selects
    const [selectedFile, setSelectedFile] = useState<File | null>(null);

    //stores image preview link
    const [previewUrl, setPreviewUrl] = useState("");

    //stores prediction result
    const [prediction, setPrediction] = useState<Prediction | null>(null);
    useScrollReveal(uploadRef, prediction?.prediction_id ?? "");

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
    }

    //analyze button activate
    function handleAnalyzeClick() {
        if (!selectedFile){return;}

        const fakePrediction = {
            prediction_id: "pred_fake_001",
            plant_state: "dry_wilting",
            possible_condition: "possible_water_stress",
            confidence: 0.82,
            severity: "medium",
            suggestion:
            "Check soil moisture. If the soil is dry, water the plant and monitor it over the next few days.",
            model_version: "plant-health-v0-fake",
            needs_review: false,
        }
        setPrediction(fakePrediction);
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
        <button onClick={handleAnalyzeClick}>
          Analyze Plant
        </button>
      </div>

      {/* This shows the prediction after Analyze is clicked */}
      <PredictionCard prediction={prediction} />
    </section>
  );
}
