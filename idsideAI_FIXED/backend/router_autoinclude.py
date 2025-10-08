# router_autoinclude.py
# Minimal helper to auto-include FastAPI routers discovered under a package.
# Usage in main.py:
#     from router_autoinclude import autoload_routers
#     autoload_routers(app, "backend.routers")
from importlib import import_module
import pkgutil

def autoload_routers(app, base_pkg: str) -> int:
    # Dynamically import all modules under `base_pkg` and include any `router` attr.
    found = 0
    pkg = import_module(base_pkg)
    for mod in pkgutil.walk_packages(pkg.__path__, pkg.__name__ + "."):
        try:
            m = import_module(mod.name)
            r = getattr(m, "router", None)
            if r is not None:
                app.include_router(r)
                found += 1
        except Exception as e:
            # Non-fatal: keep startup resilient
            print(f"[router_autoinclude] skip {mod.name}: {e}")
    print(f"[router_autoinclude] routers included: {found}")
    return found
