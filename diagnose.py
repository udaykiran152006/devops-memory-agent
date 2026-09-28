import json

PROMPT = """You are a DevOps agent. Given this error and past similar failures,
return ONLY JSON with keys: root_cause (specific, not generic), confidence (0-1),
fix_steps (list of strings), risk_level (low/medium/high).

ERROR: {error}

PAST SIMILAR FAILURES: {past}
"""

FALLBACK = {
    "dependency": "A package is missing or has a version conflict",
    "test_failure": "A test is failing after a recent change",
    "config": "An environment variable or config value is missing",
    "permissions": "Credentials or permissions are insufficient",
    "infra": "Network, timeout or resource problem",
    "unknown": "Cause unclear, needs manual review",
}

def diagnose(parsed, past):
    try:
        import anthropic  # needs ANTHROPIC_API_KEY in the environment
        client = anthropic.Anthropic()
        r = client.messages.create(
            model="claude-sonnet-5", max_tokens=600,
            messages=[{"role": "user", "content": PROMPT.format(
                error=json.dumps(parsed), past=json.dumps(past)[:2000])}])
        text = r.content[0].text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except Exception:
        # No key or bad output: still return valid JSON so the demo never breaks
        return {"root_cause": FALLBACK[parsed["error_type"]], "confidence": 0.5,
                "fix_steps": ["Check the error message and the latest commit"],
                "risk_level": "medium"}
