"""Initialization adding a pre-root path to system's paths."""
import sys
from pathlib import Path

# Using built-in venv lib go to 4 lvl up from sit-packages of env dir
DEFAULT_ROOT_DIR = Path(__file__).resolve().parent.parent
CUSTOM_ROOT_DIR = DEFAULT_ROOT_DIR.parent

if str(CUSTOM_ROOT_DIR) not in sys.path:
    sys.path.append(str(CUSTOM_ROOT_DIR))

# pylint: disable=C0413
from .database import DBManager, KisDBManager, main
from .models import User

__all__ = ["DBManager", "KisDBManager", "main", "User", "Profile"]