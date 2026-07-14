type SuggestionCardProps = {
  possibleCondition: string;
  severity: string;
  suggestion: string;
};

const formatLabel = (value: string) =>
  value.replace(/_/g, " ").replace(/\b\w/g, (letter: string) => letter.toUpperCase());

export default function SuggestionCard({
  possibleCondition,
  severity,
  suggestion,
}: SuggestionCardProps) {
  return (
    <div className="suggestion-card">
      {/* This creates the suggestion card title */}
      <h4>Care Suggestion</h4>

      {/* This shows the possible plant condition */}
      <p>
        <strong>Possible condition:</strong> {formatLabel(possibleCondition)}
      </p>

      {/* This shows how serious the issue may be */}
      <p>
        <strong>Severity:</strong> {formatLabel(severity)}
      </p>

      {/* This shows the care advice */}
      <p>{suggestion}</p>
    </div>
  );
}
