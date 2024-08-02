#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from .parsers import main

router = APIRouter()


@router.get('/api/v1/run_parser')
async def run_parser() -> JSONResponse:
    """Start web-parser."""
    return await main()
