import sys, json
from analyzer import analyze

result = analyze(json.load(open(sys.argv[1])))
print(json.dumps(result, indent=2))
if result["seen_before"]:
    print(f"\n>> Seen {result['seen_before']} time(s) before: {result['similar_incidents']}")
else:
    print("\n>> First time seeing this failure.")
