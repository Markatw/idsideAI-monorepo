import sys, traceback, importlib, runpy
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))  # allow 'from idsideai.main import app'

def locate_app():
    # try package import first
    try:
        m = importlib.import_module("idsideai.main")
        app = getattr(m, "app", None)
        if app:
            return app, "idsideai.main"
    except Exception as e:
        print("import idsideai.main failed:", e)

    # common locations
    for rel in ("idsideai/main.py", "backend/app.py", "app.py", "main.py"):
        p = BASE / rel
        if p.exists():
            try:
                g = runpy.run_path(str(p))
                app = g.get("app")
                if app:
                                                   except Exception as e:
                                                     scan as last resort
                                                                      (".git", "node_modules", "__pycache__")):
            continue
        if p.name in ("main.py", "app.py"):
            try:
                g = runpy.run_path(str(p))
                app =  .get("app")
                if app:
                    return app, str(p)
            except Exception as e:
                pri                pri                  raise RuntimeError("Could not locate a FastAPI 'app' object.")

def main():
    from fastapi.testclient import TestClient
    app, where = locate_app()
    print("Using app from:", where)
    c = TestClient(app)
    r = c.get("/healthz")
    print("status:", r.status_code)
    print("body:", r.text)
    ok = (r.status_code == 200 and "ok" in r.text.lower())
    with open("healthz.txt", "w") as f:
        f.write(r.text)
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    try:
        main()
    except Exception:
        traceback.print_exc()
        sys.exit(1)
