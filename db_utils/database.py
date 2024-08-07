#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains DB manager interface and its implementations."""
from typing import Sequence
from sqlalchemy import create_engine, Connection, Table
from sqlalchemy.orm import sessionmaker, Session
from fms.auth.models import Base  # type: ignore
from fms.settings import settings  # type: ignore


# pylint: disable=R0903
class SessionManager:
    """
    Manages the database connection and session.

    Attributes:
        engine: Connection: The database engine connection.
        session_local: Session: The SQLAlchemy session bound
         to the engine.
    """

    def __init__(self) -> None:
        """
        Initializes the SessionManager with a database connection
        and session.

        :param settings.kis_db_url: str: The database URL from the
         settings.
        """
        self.engine: Connection = create_engine(settings.kis_db_url, echo=True).connect()
        self.session_local: Session = sessionmaker(autoflush=False, bind=self.engine)()

    def create_tables(self, tables: Sequence[Table] | None = None) -> None:
        """
        Creates database tables based on SQLAlchemy models.

        :param tables: Sequence[Table] | None: A list of specific tables
         to create. If None, all tables defined in the metadata
         are created.
        """
        if tables is None:
            Base.metadata.create_all(bind=self.engine)
        else:
            Base.metadata.create_all(bind=self.engine, tables=tables)
        self.engine.commit()
