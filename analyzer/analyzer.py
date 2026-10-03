from parser import parse_request
from diagnose import diagnose


def analyze(request, past_failures=None):
    """
    Main entry point for the analyzer. Kept independent of any memory
    implementation, as agreed with Member 3.

    Args:
        request: the raw JSON from POST /api/analyze (docs/api.md format).
        past_failures: optional list of past similar failures, already
            fetched by the integration layer via backend/memory.py's
            recall_failures(). Each item is expected to look like
            {"description": str, "fix": str} (confirm exact shape with
            team lead / docs/api.md). Pass None or [] if none available.

    Returns:
        dict with the diagnosis, PLUS a "to_retain" field: a ready-made
        description + fix string that the integration layer can pass to
        backend/memory.py's store_failure() after this call, so the
        analyzer never calls memory functions itself.
    """
    past_failures = past_failures or []
    parsed = parse_request(request)
    diagnosis = diagnose(parsed, past_failures)

    description = (f"[{parsed['service']}] {parsed['error_type']} at stage "
                    f"{parsed['stage']}: {parsed['message']}")
    fix = "; ".join(diagnosis.get("fix_steps", []))

    return {
        "run_id": parsed["run_id"],
        "error_type": parsed["error_type"],
        "root_cause": diagnosis.get("root_cause"),
        "confidence": diagnosis.get("confidence"),
        "fix_steps": diagnosis.get("fix_steps"),
        "risk_level": diagnosis.get("risk_level"),
        "seen_before": len(past_failures),
        "to_retain": {"description": description, "fix": fix},
    }  
