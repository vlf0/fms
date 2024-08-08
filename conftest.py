"""Description `parser` module tests setups as a fixtures."""
import os
from typing import AsyncGenerator
import pytest
from pytest import FixtureRequest
from playwright.async_api import async_playwright, Browser, BrowserContext
from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
from auth.models import Base
from fms.main import app
from auth import AuthHandler
from auth.schemas import UserCreate, UserLogin


class TestPlaywrightSetup:
    """
    Class grouping tests setups by relationship
    to playwright functionality.
    """

    @pytest.fixture(scope='class')
    def get_url(self, request: FixtureRequest) -> None:
        """
        Create and provide a Playwright browser instance.

        :return: An AsyncGenerator yielding a Browser instance.
        :raises RuntimeError: If the browser fails to launch.
        """
        request.cls.url = 'https://google.com'

    @pytest.fixture
    async def create_browser(self) -> AsyncGenerator[Browser, None]:
        """
        Create and provide a Playwright browser instance.

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

        :return: An AsyncGenerator yielding a BrowserContext instance.
        :raises RuntimeError: If the browser or context fails to be created.
        """
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            async with browser as b:
                context: BrowserContext = await b.new_context()
                yield context
