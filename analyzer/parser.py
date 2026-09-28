import re

RULES = [
    ("dependency",  ["ERESOLVE", "ModuleNotFound", "Cannot find module", "No matching distribution"]),
    ("config",      ["undefined", "KeyError", "environment variable", "not set"]),
    ("permissions", ["denied", "403", "Forbidden", "EACCES"]),
    ("infra",       ["timeout", "timed out", "ECONNREFUSED", "unreachable", "out of memory", "OOM"]),
    ("test_failure",["FAILED", "AssertionError", "tests failed"]),
]

def classify(text):
    t = text.lower()
    for label, words in RULES:
        if any(w.lower() in t for w in words):
            return label
    return "unknown"

def parse_request(req):
    """Turns the POST /api/analyze request (docs/api.md) into a flat dict."""
    pipeline = req.get("pipeline", {})
    logs = req.get("logs", {})
    error = logs.get("error") or logs.get("raw", "")
    return {
        "run_id": req.get("run_id", "unknown"),
        "service": pipeline.get("name", "unknown"),
        "provider": pipeline.get("provider", "unknown"),
        "branch": pipeline.get("branch", "unknown"),
        "commit": pipeline.get("commit", "unknown"),
        "stage": req.get("stage", "unknown"),
        "timestamp": req.get("timestamp", "unknown"),
        "message": error.strip(),
        "error_type": classify(logs.get("raw", "") + " " + error),
    }
