from parser import parse_request
from diagnose import diagnose
from memory_adapter import recall, retain

def analyze(request):
    """Main entry point. Input: request JSON from docs/api.md. Output: dict."""
    parsed = parse_request(request)
    past = recall(parsed)
    diagnosis = diagnose(parsed, past)
    retain(parsed, diagnosis)
    return {
        "run_id": parsed["run_id"],
        "error_type": parsed["error_type"],
        "root_cause": diagnosis.get("root_cause"),
        "confidence": diagnosis.get("confidence"),
        "fix_steps": diagnosis.get("fix_steps"),
        "risk_level": diagnosis.get("risk_level"),
        "seen_before": len(past),
        "similar_incidents": [p["parsed"]["run_id"] for p in past],
    }
