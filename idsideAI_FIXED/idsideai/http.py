import httpx, asyncio

_client: httpx.AsyncClient | None = None

async def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
        _client = httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=3.0), limits=limits)
    return _client

async def aget(url, **kw):
    cl = await get_client()
    for attempt in range(3):
        try:
            return await cl.get(url, **kw)
        except httpx.RequestError:
            if attempt == 2:
                raise
            await asyncio.sleep(0.25 * (2 ** attempt))

async def shutdown():
    global _client
    if _client is not None:
        await _client.aclose()
        _client = None
