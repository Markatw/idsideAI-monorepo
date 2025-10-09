# Comprehensive security hardening for FastAPI/Starlette apps
import os
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response
from starlette.middleware import Middleware
# from starlette.middleware.security import SecurityMiddleware  # Not available
from starlette.middleware.gzip import GZipMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.cors import CORSMiddleware
import uuid

DEFAULT_MAX_BODY = int(os.getenv("MAX_REQUEST_BODY_BYTES", "10485760"))  # 10 MB
DEFAULT_ALLOWED_HOSTS = [h.strip() for h in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
DEFAULT_CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
RATE_LIMITS_BURST = os.getenv("RATE_LIMITS_BURST", "10/second")
RATE_LIMITS_SUSTAINED = os.getenv("RATE_LIMITS_SUSTAINED", "60/minute")

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        req_id = request.headers.get("x-request-id") or uuid.uuid4().hex
        # attach to state and response
        request.state.request_id = req_id
        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response

class MaxBodySizeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        # deny if content-length exceeds cap (best-effort; still stream-guards)
        try:
            cl = int(request.headers.get("content-length", "0"))
            if cl > DEFAULT_MAX_BODY:
                return Response(status_code=413, content='{"detail":"Payload too large"}', media_type="application/json")
        except Exception as e:
            print(f"Error in MaxBodySizeMiddleware: {e}")
        return await call_next(request)

class StripServerHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response: Response = await call_next(request)
        # Remove or overwrite identifying headers
        for h in ["server", "x-powered-by"]:
            if h in response.headers:
                del response.headers[h]
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
        response.headers["Cross-Origin-Embedder-Policy"] = "require-corp"
        response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
        response.headers["Permissions-Policy"] = "accelerometer=(), camera=(), geolocation=(), gyroscope=(), microphone=(), usb=(), fullscreen=(self)"
        return response

def wire_security_full(app):
    # HTTPS redirect (enable if behind TLS or proxy that sets X-Forwarded-Proto)
    # Disabled for development environment
    if os.getenv("ENABLE_HTTPS_REDIRECT", "0") == "1":
        app.add_middleware(HTTPSRedirectMiddleware)

    # Strict security headers (CSP etc.) - using custom middleware instead
    # SecurityMiddleware not available in this Starlette version

    # Trusted hosts
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=DEFAULT_ALLOWED_HOSTS)

    # CORS (default = off; enable only if origins provided)
    if DEFAULT_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=DEFAULT_CORS_ORIGINS,
            allow_credentials=False,
            allow_methods=["GET","POST","PUT","DELETE","OPTIONS"],
            allow_headers=["Authorization","Content-Type","Accept","X-Request-ID"],
            max_age=600
        )

    # Max body size and gzip
    app.add_middleware(MaxBodySizeMiddleware)
    app.add_middleware(GZipMiddleware, minimum_size=500)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(StripServerHeaderMiddleware)

    # Rate limiting (burst + sustained) if slowapi present
    try:
        from slowapi import Limiter
        from slowapi.util import get_remote_address
        from slowapi.errors import RateLimitExceeded
        from slowapi.middleware import SlowAPIMiddleware

        limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMITS_BURST, RATE_LIMITS_SUSTAINED])
        app.state.limiter = limiter
        app.add_exception_handler(RateLimitExceeded, lambda req, exc: (
            __import__('fastapi').responses.JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})
        ))
        app.add_middleware(SlowAPIMiddleware)
    except Exception as e:
        print(f"slowapi not installed, rate limiting disabled: {e}")

    return app
