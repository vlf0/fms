#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains endpoints to users register and login."""
from fastapi import APIRouter
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
    return await UserAuthenticate.create_user(user)


@router.post('/api/v1/login')
async def login_user(user: UserLogin) -> JSONResponse:
    """
    Authenticates a user and returns a JWT token.

    :param user: UserLogin: The user login credentials.
    :return: JSONResponse: The response containing the JWT token
     if authentication is successful.
    """
    return await UserAuthenticate.authenticate_user(user)
