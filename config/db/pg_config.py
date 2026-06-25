import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(PROJECT_ROOT / ".env")


def get_pg_config():
    """PostgreSQL connection settings for the dashboard (independent of Django's DB)."""
    return {
        "NAME": os.environ.get("PG_NAME", "postgres"),
        "USER": os.environ.get("PG_USER", "postgres"),
        "PASSWORD": os.environ.get("PG_PASSWORD", ""),
        "HOST": os.environ.get("PG_HOST", "localhost"),
        "PORT": os.environ.get("PG_PORT", "5432"),
    }
