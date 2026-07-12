export default function SuggestionCard({possibleCondition, severity, suggestion}: {possibleCondition: string, severity: string, suggestion: string}) {

    return (
    <div className="suggestion-card">
      {/* This creates the suggestion card title */}
      <h4>Care Suggestion</h4>

      {/* This shows the possible plant condition */}
      <p>
        <strong>Possible condition:</strong> {possibleCondition}
      </p>

      {/* This shows how serious the issue may be */}
      <p>
        <strong>Severity:</strong> {severity}
      </p>

      {/* This shows the care advice */}
      <p>{suggestion}</p>
    </div>
  );
}