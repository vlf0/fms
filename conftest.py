#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description `parser` module tests setups as a fixtures."""
import os
from typing import AsyncGenerator, Generator

import pytest
from pytest import FixtureRequest
from playwright.async_api import async_playwright, Browser, BrowserContext
from sqlalchemy import Connection
from fastapi.testclient import TestClient

from main import app
from db_utils import session_manager
from auth.models import Base


class TestAuthSetup:
    """
    Fixtures for setting up and tearing down authentication-related
    test environments.
    """

    @pytest.fixture(scope='module')
    def get_db(self) -> Generator[None, None, None]:
        """
        Set up and tear down the database for tests.

        This fixture creates the database schema before tests are run
        and drops the schema after tests are completed. It is scoped
        to the module, meaning it runs once per module.
        """
        if not os.getenv('TESTING', ''):
            raise ValueError('"TESTING" env variable was not found.')
        engine: Connection = session_manager.engine
        Base.metadata.create_all(bind=engine)
        engine.commit()
        yield
        Base.metadata.drop_all(bind=engine)
        engine.commit()
        engine.close()

    @pytest.fixture
    def client(self) -> Generator[TestClient, None, None]:
        """
        Create and provide a FastAPI TestClient instance.

        This fixture initializes the TestClient for making requests to
        the FastAPI application. It is used for sending HTTP requests
        and receiving responses in tests.
        """
        with TestClient(app) as client:
            yield client


class TestPlaywrightSetup:
    """
    Class grouping test setups related to Playwright functionality.
    """

    @pytest.fixture(scope='class')
    def get_url(self, request: FixtureRequest) -> None:
        """
        Provide a base URL for Playwright tests.

        This fixture sets a base URL for Playwright tests. It is scoped
        to the class, meaning it runs once per test class.

        :param request: FixtureRequest: The request object for
         the fixture.
        """
        request.cls.url = 'https://google.com'

    @pytest.fixture
    async def create_browser(self) -> AsyncGenerator[Browser, None]:
        """
        Create and provide a Playwright browser instance.

        This fixture launches a Playwright browser instance for use in
        tests. It is an asynchronous generator that yields the browser
        instance and ensures proper cleanup after tests are completed.

        :return: An AsyncGenerator yielding a Browser instance.
        :raises RuntimeError: If the browser fails to launch.
        """
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            yield browser

    @pytest.fixture
    async def create_context(self) -> AsyncGenerator[BrowserContext, None]:
        """
        Create and provide a Playwright browser context.

        This fixture creates a Playwright browser context, which can be
        used to manage browser sessions and state. It is an asynchronous
        generator that yields the browser context and ensures proper
        cleanup after tests are completed.

        :return: An AsyncGenerator yielding a BrowserContext instance.
        :raises RuntimeError: If the browser or context fails
         to be created.
        """
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            async with browser as b:
                context: BrowserContext = await b.new_context()
                yield context
