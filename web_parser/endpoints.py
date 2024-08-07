#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
# pylint: disable=E0401
from auth import AuthHandler
from .main import hh_parser

router = APIRouter()


@router.post('/api/v1/run_parser')
# pylint: disable=W0613
async def run_parser(check: str = Depends(AuthHandler.check_auth)) -> JSONResponse:
    """Start web-parser."""
    return await hh_parser()
