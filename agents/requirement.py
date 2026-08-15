def analyze(requirement, context):
    return {
        "status": "HUMAN_CLARIFICATION_REQUIRED",
        "business_objective": "Improve store-manager visibility and reduce stockout risk.",
        "user_story": "As a store manager, I want timely visibility when inventory is predicted to fall below replenishment levels.",
        "acceptance_criteria": [
            "Identify products predicted to fall below threshold within horizon.",
            "Notify relevant store manager.",
            "Do not automatically create an order without explicit approval."
        ],
        "ambiguities": [
            "Definition of high-demand",
            "Replenishment threshold",
            "Forecast horizon",
            "Notification versus automatic order creation"
        ],
        "risk": "MEDIUM",
        "grounding": ["business_context.md", "architecture.md", "nfr.md"]
    }

def approve(answers):
    return {
        "status": "READY_FOR_DESIGN",
        "business_objective": "Improve store-manager visibility and reduce stockout risk.",
        "user_story": "As a store manager, I want timely visibility when inventory is predicted to fall below replenishment levels.",
        "acceptance_criteria": [
            "Identify products predicted to fall below threshold within horizon.",
            "Notify relevant store manager.",
            "Do not automatically create an order without explicit approval."
        ],
        "clarifications": answers,
        "assumptions": []
    }
