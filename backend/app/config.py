import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODEL_ROOT = PROJECT_ROOT / "models"

MODEL_THRESHOLD = 0.49
MODEL_MAX_LENGTH = 128

CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "CORS_ORIGINS",
        ("http://localhost:5173,http://127.0.0.1:5173"),
    ).split(",")
    if origin.strip()
]
