import json, sys, urllib.request
BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8013"
req = urllib.request.Request(f"{BASE}/openapi.json")
with urllib.request.urlopen(req, timeout=5) as r:
    spec = json.load(r)
paths = set(spec.get("paths", {}).keys())
required = {
    "/org/dev-seed",
    "/policy/packs",
    "/billing/plans",
    "/analytics/overview",
    "/inbox",
    "/compose/schema",
}
missing = sorted(required - paths)
if missing:
    print("Missing required routes:", missing)
    sys.exit(1)
print("OpenAPI guard passed.")
