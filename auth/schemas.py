#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description schemas of auth service."""
from pydantic import BaseModel


class UserCreate(BaseModel):
    """
    Schema for user registration.

    Attributes:
        email: str: The email address of the user.
        name: str: The name of the user.
        password: str: The password chosen by the user.
    """
    email: str
    name: str
    password: str


class UserLogin(BaseModel):
    """
    Schema for user login.

    Attributes:
        name: str: The name of the user.
        password: str: The password of the user.
    """
    name: str
    password: str
