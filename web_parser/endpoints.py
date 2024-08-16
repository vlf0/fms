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
    """
    Starts the web parser and returns the parsed data as a response.

    :param check: A dependency that checks if the user is authenticated.
    :return: A JSON response containing the parsed data or task status.
    """
    response = await CacheManager().response_result()
    return response
