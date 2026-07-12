type ConfidenceBadgeProps = {
    confidence: number;
};

export default function ConfidenceBadge({ confidence }: ConfidenceBadgeProps) {
    const confidencePercentage = Math.round(confidence * 100);
    let badgeClass = "confidence-badge low-confidence";

    if (confidencePercentage >= 80) {
        badgeClass = "confidence-badge high-confidence";
    } else if (confidencePercentage >= 60) {
        badgeClass = "confidence-badge medium-confidence";
    }
    return (
        <span className={badgeClass}>
            {confidencePercentage}% confidence
        </span>
    );
}
