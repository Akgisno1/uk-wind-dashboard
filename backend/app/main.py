import logging
import os
import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("wind.api")

app = FastAPI(title="Wind Forecast Portal")

# Local dev origins plus any Vercel preview/production domain.
# Extra origins can be added with a comma-separated ALLOWED_ORIGINS env var.
allowed_origins = [
    origin.strip()
    for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """One log line per API call, visible in the Vercel runtime logs."""
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception:
        logger.exception("FAILED %s %s", request.method, request.url.path)
        raise

    duration_ms = (time.perf_counter() - started) * 1000
    logger.info(
        "%s %s -> %d (%.1f ms) origin=%s",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
        request.headers.get("origin", "-"),
    )
    return response


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
