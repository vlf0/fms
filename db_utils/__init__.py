#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Initializes a database session using the SessionManager class."""
import os
import sys
from pathlib import Path

# Using built-in venv lib go to 4 lvl up from sit-packages of env dir
DEFAULT_ROOT_DIR = Path(__file__).resolve().parent.parent
CUSTOM_ROOT_DIR = DEFAULT_ROOT_DIR.parent

if str(CUSTOM_ROOT_DIR) not in sys.path:
    sys.path.append(str(CUSTOM_ROOT_DIR))

# pylint: disable=C0413
from .database import SessionManager

session_manager: SessionManager = SessionManager()

__all__ = ['session_manager']
