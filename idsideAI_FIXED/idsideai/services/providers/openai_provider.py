from __future__ import annotations
import os, anyio
from typing import Optional
try:
    from openai import OpenAI
except Exception:
    OpenAI = None
class OpenAIError(RuntimeError): ...
async def run_openai(prompt: str, model: str, api_key: Optional[str]) -> str:
    if not api_key: raise OpenAIError("OPENAI_API_KEY is not configured.")
    if OpenAI is None: raise OpenAIError("OpenAI SDK is not installed in this virtualenv.")
    def _call():
        client = OpenAI(api_key=api_key)
        r = client.chat.completions.create(model=model or "gpt-4o",
                                           messages=[{"role":"user","content":prompt}],max_tokens=256)
        return (r.choices[0].message.content or "").strip()
    try:
        return await anyio.to_thread.run_sync(_call)
    except Exception as e:
        if os.getenv("OPENAI_FALLBACK","1") in ("1","true","True"):
            return f"[OPENAI_FALLBACK] {prompt}"
        raise OpenAIError(f"OpenAI call failed: {e}") from e
