# Security utilities (safe evaluation and middleware wiring)

import ast
from typing import Any

def safe_eval(value: Any):
    """Safely evaluate Python literals only. Raises ValueError for anything else."""
    if isinstance(value, (bytes, bytearray)):
        value = value.decode('utf-8', errors='ignore')
    if not isinstance(value, str):
        # Already a non-string; just return it (no dynamic eval semantics)
        return value
    try:
        return ast.literal_eval(value)
    except Exception as e:
        raise ValueError("Unsafe or invalid expression supplied to safe_eval") from e

def wire_security(app):
    """Attach SecurityMiddleware and optional rate limiting to a FastAPI app.
    - Security headers via Starlette SecurityMiddleware
    - Rate limiting via slowapi if installed (default 100/min per IP)
    """
    try:
        from starlette.middleware import Middleware
        from starlette.middleware.sessions import SessionMiddleware
        from starlette.middleware import Middleware as _M  # just to avoid lints
        from starlette.middleware.trustedhost import TrustedHostMiddleware
        from starlette.middleware.gzip import GZipMiddleware
        from starlette.middleware.cors import CORSMiddleware
        from starlette.middleware import Middleware as MiddlewareClass
        from starlette.middleware import base as base_mw
        from starlette.middleware import errors as errors_mw
        from starlette.middleware import httpsredirect
        from starlette.middleware.security import SecurityMiddleware
    except Exception:
        # Minimal import path; SecurityMiddleware is the key
        from starlette.middleware.security import SecurityMiddleware

    # Security headers
    app.add_middleware(
        SecurityMiddleware,
        content_security_policy="; ".join([
            "default-src 'self'",
            "style-src 'self' 'unsafe-inline'",
            "script-src 'self'",
            "img-src 'self' data:"
        ]),
        content_security_policy_report_only=False,
        referrer_policy="no-referrer",
        strict_transport_security="max-age=31536000; includeSubDomains",
        x_content_type_options="nosniff",
        x_frame_options="DENY"
    )

    # Optional: rate limiting via slowapi
    try:
        from slowapi import Limiter
        from slowapi.util import get_remote_address
        from slowapi.errors import RateLimitExceeded
        from slowapi.middleware import SlowAPIMiddleware

        limiter = Limiter(key_func=get_remote_address, default_limits=["100/minute"])  # tune as needed
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, lambda req, exc: (
            __import__('fastapi').responses.JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        ))
        app.add_middleware(SlowAPIMiddleware)
    except Exception as e:
        print(f"slowapi not installed, rate limiting disabled: {e}")

    # Optional gzip
    try:
        from starlette.middleware.gzip import GZipMiddleware
        app.add_middleware(GZipMiddleware, minimum_size=500)
    except Exception as e:
        print(f"GZipMiddleware not available: {e}")

    return app
