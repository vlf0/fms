#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains user registration / authentication logic."""
from datetime import timedelta
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fms.db_utils import session  # type: ignore
from .schemas import UserCreate, UserLogin
from .models import User
from .auth_handler import AuthHandler, ACCESS_TOKEN_EXPIRE_MINUTES


class UserAuthenticate:
    """
    Service class for user authentication and registration.

    Provides methods to create a new user and authenticate existing users.
    """

    @staticmethod
    async def create_user(user: UserCreate) -> JSONResponse:
        """
        Registers a new user in the system.

        :param user: UserCreate: The user registration data.
        :return: JSONResponse: A response indicating the result of the registration process.
        :raises HTTPException: If the user already exists.
        """
        with session as s:
            user_instance = (s.query(User)
                             .filter(User.email == user.email)
                             .first())
            if user_instance is None:
                hashed_password = AuthHandler.get_password_hash(user.password)
                print('save to db pass: ', hashed_password)
                new_user = User(name=user.name,  # type: ignore
                                password=hashed_password,
                                email=user.email,
                                is_active=True,
                                is_stuff=False)
                s.add(new_user)
                s.commit()
                return JSONResponse(status_code=status.HTTP_201_CREATED,
                                    content={'message': 'User created successfully'})
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail='User already exists!')

    @staticmethod
    async def authenticate_user(user: UserLogin) -> JSONResponse:
        """
        Authenticates a user and returns a JWT token.

        :param user: UserLogin: The user login credentials.
        :return: JSONResponse: A response containing the JWT token if authentication is successful.
        :raises HTTPException: If the credentials are invalid.
        """
        with session as s:
            user_instance = (s.query(User)
                             .filter(User.name == user.name)
                             .first())
            if user_instance is None or not AuthHandler.verify_password(
                    user.password,
                    user_instance.password):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Invalid credentials')
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = AuthHandler.create_access_token(
                data={'sub': user.name}, expires_delta=access_token_expires
            )
            response = JSONResponse(status_code=status.HTTP_200_OK,
                                    content={'message': 'coockie sended'})
            response.set_cookie(key='token',
                                value=access_token,
                                expires=259200,
                                httponly=True,
                                domain='localhost',
                                )
            print(access_token)
            return response
