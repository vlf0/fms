#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Class to authenticate and JWT token generation."""
import datetime
from datetime import timedelta
from typing import Dict, Any
import jwt
from jwt.exceptions import ExpiredSignatureError, PyJWTError
import bcrypt
from fastapi import HTTPException, status
from fms.settings import settings  # type: ignore


SECRET_KEY = settings.jwt_secret_key
ALGORITHM = "HS256"
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
            expire = datetime.datetime.now(datetime.UTC) + expires_delta
        else:
            expire = (datetime.datetime.now(datetime.UTC)
                      + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"iat": int(expire.timestamp())})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_access_token(token: str) -> dict[str, Any]:
        """
        Decodes a JWT token and returns the payload.

        :param token: str: The JWT token to decode.
        :return: dict[str, Any]: The decoded payload.
        :raises HTTPException: If the token has expired or is invalid.
        """
        try:
            payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except ExpiredSignatureError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Token has expired") from exc
        except PyJWTError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials") from exc
