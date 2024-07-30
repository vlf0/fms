"""Contains tests for `parse` module checking."""
import pytest
from typing import AsyncGenerator
from fms.conftest import TestPlaywrightSetup  # type: ignore
from playwright.async_api import BrowserContext, Page, Browser
from .parsers import BaseParser, USER_AGENTS
from .soups import BaseSoup


@pytest.mark.asyncio
@pytest.mark.usefixtures('get_url')
class TestSoups(TestPlaywrightSetup):  # type: ignore
    """
    Class grouping tests by relationship
    to playwright functionality.
    """

    async def test_create_context_correct(
            self,
            create_browser: AsyncGenerator[Browser, None]
    ) -> None:
        """
        Tests the creation of a browser context using
        a valid browser instance.

        This test verifies that a valid `Browser` instance can be used
        to create a `BrowserContext` and checks if the returned context
        is of the correct type.

        :param create_browser: An asynchronous generator that provides a
         `Browser` instance.
        :return: None
        :raises AssertionError: If the created context is not
         an instance of `BrowserContext`.
        """
        async for browser in create_browser:
            context = await BaseParser(self.url)._create_context(browser)
            assert isinstance(context, BrowserContext)

    async def test_create_context_untransferred(self) -> None:
        """
        Tests the creation of a browser context when no browser instance
        is provided.

        This test ensures that attempting to create a `BrowserContext`
        without providing a `Browser` instance raises a `TypeError`.

        :return: None
        :raises TypeError: If no `Browser` instance is provided.
        """
        with pytest.raises(TypeError):
            await BaseParser(self.url)._create_context()  # type: ignore

    async def test_create_context_incorrect_type(self) -> None:
        """
        Tests the creation of a browser context when an incorrect type
        is provided.

        This test verifies that providing an invalid type
        (e.g., an integer) instead of a `Browser` instance raises
        an `AttributeError`.

        :return: None
        :raises AttributeError: If an invalid type is provided instead
         of a `Browser` instance.
        """
        with pytest.raises(AttributeError):
            await BaseParser(self.url)._create_context(1)  # type: ignore

    async def test_create_page_correct(
            self,
            create_context: AsyncGenerator[BrowserContext, None]
    ) -> None:
        """
        Tests the creation of a page using a valid browser context.

        This test verifies that a valid `BrowserContext` instance can be
        used to create a `Page` and checks if the returned page is
        of the correct type.

        :param create_context: An asynchronous generator that provides
         a `BrowserContext` instance.
        :return: None
        :raises AssertionError: If the created page is not an instance
         of `Page`.
        """
        async for context in create_context:
            page = await BaseParser(self.url)._create_page(context)
            assert isinstance(page, Page)

    async def test_create_page_untransferred(self) -> None:
        """
        Tests the creation of a page when no browser context
        is provided.

        This test ensures that attempting to create a `Page` without
        providing a `BrowserContext` instance raises a `TypeError`.

        :return: None
        :raises TypeError: If no `BrowserContext` instance is provided.
        """
        with pytest.raises(TypeError):
            await BaseParser(self.url)._create_page()  # type: ignore

    async def test_create_page_incorrect_type(self) -> None:
        """
        Tests the creation of a page when an incorrect type is provided.

        This test verifies that providing an invalid type
        (e.g., an integer) instead of a `BrowserContext` instance
        raises an `AttributeError`.

        :return: None
        :raises AttributeError: If an invalid type is provided
         instead of a `BrowserContext` instance.
        """
        with pytest.raises(AttributeError):
            await BaseParser(self.url)._create_page(1)  # type: ignore
