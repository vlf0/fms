#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Initializes a database session using the SessionManager class."""
from .database import SessionManager

session_manager = SessionManager()

__all__ = ['session_manager']
