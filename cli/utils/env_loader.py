"""Lightweight .env loader — no third-party dependencies."""

import os
from pathlib import Path


def load_dotenv(env_path=None):
    """Load environment variables from a .env file.

    Does NOT override variables already set in os.environ.
    """
    if env_path is None:
        # cli/utils/ → cli/ → YMOS root
        env_path = Path(__file__).resolve().parents[2] / ".env"
    else:
        env_path = Path(env_path)

    if not env_path.exists():
        return

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value
