CARE_RULES = {
    "healthy" : {
        "condition" : "no_obvious_issues",
        "suggestion" : "Continue current care routine",
        "severity" : "low",
        },
    "dry-wilting": {
        "condition" : "possible_underwatering",
        "suggestion" : "Check soil moisture. If dry, water the plant and monitor it.",
        "severity" : "medium",
        },
    "yellowing": {
        "condition" : "possible_watering)light_or_nutrient_stress",
        "suggestion" : "Check watering schedule, drainage, and light exposure",
        "severity" : "medium",
        },
     "leaf_spots": {
        "condition": "disease_like_leaf_spot_pattern",
        "suggestion": "Monitor whether spots spread, avoid wetting leaves, and consider separating the plant from nearby plants.",
        "severity": "medium",
    },
    "brown_edges": {
        "condition": "possible_dryness_heat_or_salt_stress",
        "suggestion": "Check watering consistency, heat exposure, and direct light.",
        "severity": "medium",
    },
    "severe_damage": {
        "condition": "advanced_stress_or_damage",
        "suggestion": "Manual review recommended.",
        "severity": "high",
    },
    "uncertain": {
        "condition": "unclear_image_or_low_confidence",
        "suggestion": "Upload a clearer photo in natural light with the plant centered.",
        "severity": "unknown",
    },
    }

def get_care_suggestion(plant_state: str) -> dict:
    """
    Retrieve care suggestion based on the plant state.

    Args:
        plant_state (str): The state of the plant.

    Returns:
        dict: A dictionary containing the condition, suggestion, and severity.
    """
    return CARE_RULES.get(plant_state, CARE_RULES["uncertain"])