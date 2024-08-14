#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse

from .schemas import UserCreate, UserLogin
from .services import UserAuthenticate

router = APIRouter()
AuthService = Annotated[UserAuthenticate, Depends(UserAuthenticate)]


@router.post('/api/v1/register')
async def register_user(user: UserCreate, auth_process: AuthService) -> JSONResponse:
    """
    Registers a new user.

    :param user: UserCreate: The user information required
     for registration.
    :param auth_process: UserAuthenticate: Class - authenticate
     and authorization manager providing matching functional.
    :return: JSONResponse: The response indicating the result
     of the registration process.
    """
    return await auth_process.create_user(user)


@router.post('/api/v1/login')
async def login_user(user: UserLogin, auth_process: AuthService) -> JSONResponse:
    """
    Authenticates a user and returns a JWT token.

    :param user: UserLogin: The user login credentials.
    :param auth_process: UserAuthenticate: Class - authenticate
     and authorization manager providing matching functional.
    :return: JSONResponse: A JSON response containing the JWT token
     if authentication is successful.
    """
    return await auth_process.authenticate_user(user)


@router.post('/api/v1/check_user')
async def check_user(request: Request, auth_process: AuthService) -> JSONResponse:
    """
    Checks if the user is authenticated based on the JWT token in
    the request.

    :param request: Request: The HTTP request containing the JWT token
     in cookies.
    :param auth_process: UserAuthenticate: Class - authenticate
     and authorization manager providing matching functional.
    :return: JSONResponse: A JSON response indicating whether the user
     is authenticated.
    """
    return await auth_process.check_user_authorizing(request)


@router.post('/api/v1/logout')
async def logout_user(request: Request, auth_process: AuthService) -> JSONResponse:
    """
    Logs out the user by revoking the JWT token and clearing it
     from cookies.

    :param request: Request: The HTTP request to process the logout.
    :param auth_process: UserAuthenticate: Class - authenticate
     and authorization manager providing matching functional.
    :return: JSONResponse: A JSON response confirming logout success.
    """
    return await auth_process.logout_user(request)
