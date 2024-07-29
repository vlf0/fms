#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Initialization adding a pre-root path to system's paths."""
import sys
from pathlib import Path

DEFAULT_ROOT_DIR = Path(__file__).resolve().parent.parent
CUSTOM_ROOT_DIR = DEFAULT_ROOT_DIR.parent

if str(CUSTOM_ROOT_DIR) not in sys.path:
    sys.path.append(str(CUSTOM_ROOT_DIR))

# pylint: disable=C0413
from .soups import BaseSoup, HHSoup
from .parsers import BaseParser, HHParser, HH_URL

__all__ = ["BaseSoup", "HHSoup", "BaseParser", "HHParser", "HH_URL"]
