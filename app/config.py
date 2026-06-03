"""Application configuration."""

from __future__ import annotations

import os
from pathlib import Path


def _load_env_from_root() -> None:
    root = Path(__file__).resolve().parent.parent
    env_path = root / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_from_root()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "cinema")
RECEIPTS_DIR = os.getenv("RECEIPTS_DIR", "receipts")

if not MONGO_URI:
    raise RuntimeError("MONGO_URI es obligatorio. Configurelo en .env o en su consola.")
