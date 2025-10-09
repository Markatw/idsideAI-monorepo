import json, sys, urllib.request
from collections import defaultdict

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8013"

WHITELIST = {
    "/", "/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc",
    "/health", "/healthz", "/_debug/routes", "/exports",
}

EXPECTED_PREFIXES = {
    "/org", "/policy", "/billing", "/analytics",
    "/inbox", "/compose", "/graphs", "/metrics",
}

req = urllib.request.Request(f"{BASE}/openapi.json")
with urllib.request.urlopen(req, timeout=5) as r:
    spec = json.load(r)

paths = sorted(spec.get("paths", {}).keys())
groups = defaultdict(list)
root = []

def top_segment(p):
    if p == "/":
        return "/"
    parts = [seg for seg in p.split("/") if seg]
    return "/" + parts[0] if parts else "/"

for p in paths:
    seg = top_segment(p)
    if seg in EXPECTED_PREFIXES:
        groups[seg].append(p)
    elif p in WHITELIST:
        groups["__whitelist__"].append(p)
    else:
        root.append(p)

print(f"\n== Route Prefix Audit for {BASE} ==")
print(f"Total paths: {len(paths)}\n")

for seg in sorted(groups.keys()):
    label = "whitelist" if seg == "__whitelist__" else seg
    print(f"[{label}] ({len(groups[seg])})")
    for p in groups[seg]:
        print(f"  - {p}")
    print()

if root:
    print("!! Root-level (no expected prefix) routes found:")
    for p in root:
        print(f"  - {p}")
    print()
    print("Remediation tips:")
    print("  • Add prefix in router: APIRouter(prefix='/feature')")
    print("  • Or include with prefix in app.py: app.include_router(router, prefix='/feature')")
    sys.exit(1)
else:
    print("✅ No unexpected root-level routes.")

