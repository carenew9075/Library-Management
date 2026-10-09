# ---------------------------------------------------------
# LIBRARY MANAGEMENT SYSTEM
# CONFIGURATION
# ---------------------------------------------------------

import os
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "library_management")

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

APP_NAME = "Library Management System"
APP_VERSION = "1.0"
APP_AUTHOR = "Warlock"

# ---------------------------------------------------------
# RELOAD ENVIRONMENT
# ---------------------------------------------------------

def reload_environment():
    global DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
    global GEMINI_MODEL, GEMINI_API_KEY

    load_dotenv(ENV_FILE, override=True)

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "library_management")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
