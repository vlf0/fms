#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class to authenticate and JWT token generation."""
import datetime
from datetime import timedelta, timezone
from typing import Dict, Any
import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
import bcrypt
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from settings import settings


SECRET_KEY = settings.jwt_secret_key
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthHandler:
    """
    A class used to handle authentication and JWT token generation.
    """

    crypter = bcrypt

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verifies that the plain password matches the hashed password.

        :param plain_password: str: The plain text password to verify.
        :param hashed_password: str: The hashed password
         to compare against.
        :return: bool: True if the password matches, False otherwise.
        """
        pwd_bytes: bytes = plain_password.encode()
        hashed_password_bytes: bytes = hashed_password.encode()
        return AuthHandler.crypter.checkpw(password=pwd_bytes,
                                           hashed_password=hashed_password_bytes)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """
        Generates a hashed password from the plain text password.

        :param password: str: The plain text password to hash.
        :return: str: The hashed password.
        """
        salt = AuthHandler.crypter.gensalt()
        pwd_bytes = password.encode()
        hashed_password = AuthHandler.crypter.hashpw(password=pwd_bytes, salt=salt).decode()
        return hashed_password

    @staticmethod
    def create_access_token(data: Dict[str, str | datetime.datetime | int],
                            expires_delta: timedelta | None = None) -> str:
        """
        Creates a JWT access token.

        :param data: Dict[str, str | datetime.datetime]: The data
         to encode in the token.
        :param expires_delta: timedelta | None: The time duration after
         which the token will expire. Defaults to None, which sets
         the expiration to ACCESS_TOKEN_EXPIRE_MINUTES.
        :return: str: The encoded JWT token.
        """
        to_encode = data.copy()
        if expires_delta:
            # pylint: disable=E1101
            expire = datetime.datetime.now(timezone.utc) + expires_delta
        else:
            # pylint: disable=E1101
            expire = (datetime.datetime.now(timezone.utc)
                      + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({'exp': int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str) -> dict[str, Any]:
        """
        Decodes and verifies a JWT token.

        :param token: str: The JWT token to decode.
        :return: dict[str, Any]: The decoded payload.
        :raises HTTPException: If the token has expired or is invalid.
        """
        try:
            payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            if 'sub' not in payload:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Invalid token')
            return payload
        except ExpiredSignatureError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Token has expired') from exc
        except PyJWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate credentials') from exc

    @staticmethod
    def check_auth(request: Request) -> JSONResponse:
        """
        Checks if the user is authenticated based on the JWT token
        in cookies.

        :param request: Request: The HTTP request containing
         the JWT token in cookies.
        :return: JSONResponse: A JSON response indicating whether
         the user is authenticated.
        :raises HTTPException: If the token is missing or revoked.
        """
        # pylint: disable=W0511
        # TODO: Create checking for existing user in db. Now if user is
        #  not exists, but token is not revoked - check passes
        #  success, but it is incorrect behavior
        token = request.cookies.get('auth_token')
        if token is None or token == 'revoked':
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Not authenticated')
        AuthHandler.verify_token(token)
        return JSONResponse(content={'detail': 'User is authenticated'},
                            status_code=status.HTTP_200_OK)

    @staticmethod
    # pylint: disable=W0613
    def logout_user(request: Request) -> JSONResponse:
        """
        Logs out the user by revoking the JWT token and clearing it from
        cookies.

        :param request: Request: The HTTP request to process the logout.
        :return: JSONResponse: A JSON response confirming logout success.
        """
        cookie = request.cookies.get('auth_token')
        if cookie and cookie != 'revoked':
            response = JSONResponse(content={'detail': 'Logout success.'},
                                    status_code=status.HTTP_200_OK)
            response.set_cookie(key='auth_token',
                                value='revoked',
                                expires='01.01.1970',
                                httponly=True,
                                domain='159.65.135.38')
        else:
            response = JSONResponse(content={'detail': 'User is not authorized, nothing logout.'},
                                    status_code=status.HTTP_204_NO_CONTENT)
        return response
