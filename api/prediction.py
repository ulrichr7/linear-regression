"""Compatibility entrypoint.

Use `api.main:app` as the canonical FastAPI application.
This module exists only to preserve older run commands like `uvicorn api.prediction:app`.
"""

from .main import app