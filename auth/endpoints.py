#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from .schemas import UserCreate, UserLogin
from .services import UserAuthenticate

router = APIRouter()


@router.post('/api/v1/register')
async def register_user(user: UserCreate) -> JSONResponse:
    """
    Registers a new user.

    :param user: UserCreate: The user information required
     for registration.
    :return: JSONResponse: The response indicating the result
     of the registration process.
    """
    return await UserAuthenticate().create_user(user)


@router.post('/api/v1/login')
async def login_user(user: UserLogin) -> JSONResponse:
    """
    Authenticates a user and returns a JWT token.

    :param user: UserLogin: The user login credentials.
    :return: JSONResponse: A JSON response containing the JWT token
     if authentication is successful.
    """
    return await UserAuthenticate().authenticate_user(user)


@router.post('/api/v1/check_user')
async def check_user(request: Request) -> JSONResponse:
    """
    Checks if the user is authenticated based on the JWT token in
    the request.

    :param request: Request: The HTTP request containing the JWT token
     in cookies.
    :return: JSONResponse: A JSON response indicating whether the user
     is authenticated.
    """
    return await UserAuthenticate().check_user_authorizing(request)


@router.post('/api/v1/logout')
async def logout_user(request: Request) -> JSONResponse:
    """
    Logs out the user by revoking the JWT token and clearing it from cookies.

    :param request: Request: The HTTP request to process the logout.
    :return: JSONResponse: A JSON response confirming logout success.
    """
    return await UserAuthenticate().logout_user(request)
