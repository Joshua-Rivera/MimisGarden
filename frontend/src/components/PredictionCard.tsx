import ConfidenceBadge from "./ConfidenceBadge";
import SuggestionCard from "./SuggestionCard";

export type Prediction = {
  prediction_id: string;
  plant_state: string;
  possible_condition: string;
  confidence: number;
  severity: string;
  suggestion: string;
  model_version: string;
  needs_review: boolean;
};

const formatLabel = (value: string) =>
  value.replace(/_/g, " ").replace(/\b\w/g, (letter: string) => letter.toUpperCase());

type PredictionCardProps = {
  prediction: Prediction | null;
};

export default function PredictionCard({ prediction }: PredictionCardProps) {
  if (!prediction) return null;

  return (
    <div className="prediction-card reveal-on-scroll">
      {/* This creates the top part of the prediction card */}
      <div className="prediction-header">
        <div>
          <p className="small-title">Prediction Result</p>

          {/* This shows the predicted plant state */}
          <h3>{formatLabel(prediction.plant_state)}</h3>
        </div>

        {/* This shows the confidence badge */}
        <ConfidenceBadge confidence={prediction.confidence} />
      </div>

      {/* This creates the prediction details */}
      <div className="prediction-details">
        <p>
          <strong>Prediction ID:</strong> {prediction.prediction_id}
        </p>

        <p>
          <strong>Model version:</strong> {prediction.model_version}
        </p>

        <p>
          <strong>Needs review:</strong>{" "}
          {prediction.needs_review ? "Yes" : "No"}
        </p>
      </div>

      {/* This creates the suggestion card inside the prediction card */}
      <SuggestionCard
        possibleCondition={prediction.possible_condition}
        severity={prediction.severity}
        suggestion={prediction.suggestion}
      />
    </div>
  );
}
