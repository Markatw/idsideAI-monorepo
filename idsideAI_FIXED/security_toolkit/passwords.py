# Security helpers: password hashing & verification (bcrypt via passlib)
from passlib.context import CryptContext

_pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

def hash_password(plaintext: str) -> str:
    """Return bcrypt hash for a plaintext password."""
    if plaintext is None:
        raise ValueError("password must not be None")
    return _pwd_ctx.hash(plaintext)

def verify_password(plaintext: str, hashed: str) -> bool:
    """Verify a plaintext password against a stored bcrypt hash."""
    if not hashed:
        return False
    return _pwd_ctx.verify(plaintext, hashed)
