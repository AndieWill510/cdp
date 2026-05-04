"""Minimal CDP FastAPI application.

This module intentionally exposes only a health endpoint for the initial local
Docker stack. Governance APIs should be added behind explicit route modules as
protocol and schema definitions stabilize.
"""

from __future__ import annotations

from fastapi import FastAPI

from cdp import __version__

app = FastAPI(
    title="Constitutional Decision Plane API",
    version=__version__,
    description="Local reference API for the Constitutional Decision Plane.",
)


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
