# Connects the analyzer to the real memory module built by Member 3
# (backend/memory.py: store_failure, find_similar_failures, recall_from_hindsight).
import json
from memory import store_failure, find_similar_failures, recall_from_hindsight


def _describe(parsed):
    """Turn a parsed error into one text line for memory search/storage."""
    return (f"[{parsed['service']}] {parsed['error_type']} at stage "
            f"{parsed['stage']}: {parsed['message']}")


def retain(parsed, diagnosis):
    """Save this failure and its diagnosis to ChromaDB + Hindsight."""
    description = _describe(parsed)
    fix = "; ".join(diagnosis.get("fix_steps", []))
    store_failure(description, fix)


def recall(parsed):
    """Find similar past failures for this error, using ChromaDB (fast,
    local) and falling back to Hindsight for extra long-term context."""
    query = _describe(parsed)
    similar = find_similar_failures(query, n_results=3)

    hindsight_result = recall_from_hindsight(query)
    if hindsight_result:
        similar.append({"description": str(hindsight_result), "fix": ""})

    out = []
    for item in similar:
        out.append({
            "parsed": {"error_type": parsed["error_type"],
                       "service": parsed["service"],
                       "run_id": item.get("description", "")[:40]},
            "diagnosis": {"fix_steps": [item.get("fix", "")] if item.get("fix") else []}
        })
    return out
