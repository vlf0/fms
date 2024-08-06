#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from .parsers import main
from auth.auth_handler import AuthHandler

router = APIRouter()


# @router.post('/api/v1/run_parser')
# async def run_parser(current_user: str = Depends(AuthHandler.get_current_user)) -> JSONResponse:
#     """Start web-parser."""
#     # AuthHandler.get_current_user('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNzIyODcwNzQ0fQ.wH8sRitgJWEdjXThNIHY-qF3-8Y7lOk6BRvx24KGf1Q')
#     return await main()


# @router.post('/api/v1/run_parser')
# async def run_parser(request: Request) -> JSONResponse:
#     """Start web-parser."""
#     user = AuthHandler.get_current_user(request)
#     print('User:', user)
#     return await main()


@router.post('/api/v1/check_user')
async def run_parser(request: Request) -> JSONResponse:
    """Start web-parser."""
    print(request.cookies)
    user = AuthHandler.get_current_user(request)
    print('User:', user)
    return JSONResponse(content={'ms': 'ok'})
