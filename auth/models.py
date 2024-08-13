#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description the models of app's database."""
import os

from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import Mapped, declarative_base, DeclarativeMeta, mapped_column

Base: DeclarativeMeta = declarative_base()


# pylint: disable=R0903
class User(Base):
    """Represents a user in the system."""

    __tablename__ = 'users'
    __table_args__ = {'schema': 'mm'} if not os.getenv('TESTING', '') else {}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = Column(String, unique=True, index=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_stuff: Mapped[bool] = mapped_column(default=True)
