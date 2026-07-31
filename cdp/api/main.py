"""CDP FastAPI application.

Governance routes live behind explicit route modules (see cdp/api/decisions.py)
as protocol and schema definitions stabilize.
"""

from __future__ import annotations

from fastapi import FastAPI

from cdp import __version__
from cdp.api.decisions import router as decisions_router
from cdp.api.identity import router as identity_router

app = FastAPI(
    title="Constitutional Decision Plane API",
    version=__version__,
    description="Local reference API for the Constitutional Decision Plane.",
)

app.include_router(decisions_router)
app.include_router(identity_router)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return basic process health for Docker and local smoke tests."""
    return {
        "status": "ok",
        "service": "cdp-api",
        "version": __version__,
    }


@app.get("/", tags=["system"])
def root() -> dict[str, str]:
    """Return a minimal API root response."""
    return {
        "name": "Constitutional Decision Plane API",
        "status": "draft",
        "health": "/health",
    }
