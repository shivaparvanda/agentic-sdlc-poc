def validate_architecture(design):
    if "synchronous" in design.lower() and "event-driven" not in design.lower():
        return {"status":"REVIEW_REQUIRED","reason":"Validate peak event volume, latency and consistency before committing to synchronous inventory processing."}
    return {"status":"PASS","reason":"No immediate conflict detected."}
