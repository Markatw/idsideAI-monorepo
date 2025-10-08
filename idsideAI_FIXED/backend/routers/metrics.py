from fastapi import APIRouter, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

router = APIRouter(prefix="/metrics", tags=["metrics"])
requests_total = Counter('idecide_requests_total','Total HTTP requests',['method','path','status'])
latency = Histogram('idecide_request_latency_seconds','Request latency',['path'])

@router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
