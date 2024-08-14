#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from auth import AuthHandler
from .caching import CacheManager

router = APIRouter()


@router.post('/api/v1/run_parser')
# pylint: disable=W0613
async def run_parser(check: str = Depends(AuthHandler.check_auth)) -> JSONResponse:
    """Start web-parser and return parsed data as a response."""
    response = await CacheManager().get_or_create()
    return response
