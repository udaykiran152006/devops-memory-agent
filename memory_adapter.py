# TEMPORARY in-file memory so the analyzer runs on its own.
# When Member 3 gives the Hindsight functions, replace the INSIDE of
# retain() and recall() with their calls. Keep the function names.
import json, os
FILE = "memory.json"

def _load():
    return json.load(open(FILE)) if os.path.exists(FILE) else []

def retain(parsed, diagnosis):
    data = _load()
    data.append({"parsed": parsed, "diagnosis": diagnosis})
    json.dump(data, open(FILE, "w"), indent=2)

def recall(parsed):
    """Return past failures with the same error_type and service."""
    return [d for d in _load()
            if d["parsed"]["error_type"] == parsed["error_type"]
            and d["parsed"]["service"] == parsed["service"]]
