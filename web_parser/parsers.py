#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Contains parser classes for handling web scraping with Playwright
and BeautifulSoup.
"""
import random
from abc import ABC, abstractmethod

import asyncio
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    TimeoutError as PWTimeoutError
)

from .soups import HHSoup, BaseSoup

USER_AGENTS = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/91.0.864.59 Safari/537.36 Edg/91.0.864.59',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'
    ' (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.177',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Vivaldi/4.0'
)
HH_URL = ('https://hh.ru/search/vacancy?excluded_text=%D0%BF%D1%80%D0%B5%D0%BF%D0%BE%D0%B4%D0%B0%'
          'D0%B2%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%2C+%D0%BC%D0%B5%D0%BD%D1%8F%D1%8E%D1%89%D0%B8%D1%8'
          '5&ored_clusters=true&schedule=remote&search_field=name&search_period=1&text=Python')


# pylint: disable=R0903
class AbstractParser(ABC):
    """ Abstract base class for parsers that handle web scraping. """

    def __init__(self, url: str, user_agents: tuple[str, ...]) -> None:
        """
        Initializes the AbstractParser with a URL and user agents.
        """
        super().__init__()
        self.url: str = url
        self.user_agents: tuple[str, ...] = user_agents
        self.parser_type = 'html.parser'

    @abstractmethod
    async def start_browser(self) -> BaseSoup:
        """
        Starts the browser and returns the parsed content as
        a BaseSoup instance.
        """

    @abstractmethod
    async def _create_context(self, browser: Browser) -> BrowserContext:
        """ Creates a new context in the one same browser. """

    @abstractmethod
    async def _create_page(self, context: BrowserContext) -> Page:
        """ Creates a new page in the browser context. """


# pylint: disable=R0903
class BaseParser(AbstractParser):
    """ Base parser class for handling common parsing logic. """

    # pylint: disable=R0913
    def __init__(self, url: str,
                 soup_class: type[BaseSoup] = BaseSoup,
                 tag_name: str = 'default',
                 tag_attrs: dict[str, str] | None = None,
                 user_agents: tuple[str, ...] = USER_AGENTS,
                 ) -> None:
        """
        Initializes the BaseParser with URL, soup class, tag name,
         and attributes.

        :param url: The URL to scrape.
        :param soup_class: The class to use for creating soup objects.
        :param tag_name: The tag name to search for in the HTML.
        :param tag_attrs: The attributes of the tag to search for.
        :param user_agents: A tuple of user agent strings.
        """
        super().__init__(url, user_agents)
        self.url: str = url
        self.user_agents: tuple[str, ...] = user_agents
        self.soup_class: type[BaseSoup] = soup_class
        self.tag_name: str = tag_name
        self.tag_attrs: dict[str, str] | None = tag_attrs

    async def _create_context(self, browser: Browser) -> BrowserContext:
        user_agent: str = random.choice(self.user_agents)
        context: BrowserContext = await browser.new_context(user_agent=user_agent)
        return context

    async def _create_page(self, context: BrowserContext) -> Page:
        """ Creates a new page with a random user agent. """
        page: Page = await context.new_page()
        return page

    async def start_browser(self) -> BaseSoup:
        """
        Starts the browser, navigates to the URL, and returns
         the parsed content.

        :return: An instance of BaseSoup containing the parsed content.
        :raises TimeoutError: If the page fails to load
         maximum retries.
        """
        max_retries = 3
        retries = 0
        async with async_playwright() as pw:
            browser = await pw.chromium.launch()
            context = await self._create_context(browser)
            async with browser:
                page: Page = await self._create_page(context)
                async with page as p:
                    while retries < max_retries:
                        try:
                            await p.goto(self.url)
                            await p.wait_for_load_state('load')
                            content = await p.content()
                            soup_instance = self.soup_class(content, self.parser_type)
                            return soup_instance
                        except PWTimeoutError as e:
                            retries += 1
                            print(f"Attempt {retries} failed: {e}. Retrying...")
                            await asyncio.sleep(2 * retries)
                    raise PWTimeoutError("Max retries exceeded while trying to load the page")


class HHParser(BaseParser):
    """ Parser class for handling job listings from HH.ru. """

    def __init__(self,
                 url: str,
                 soup_class: type[HHSoup] = HHSoup,
                 tag_name: str = 'div',
                 tag_attrs: dict[str, str] | None = None
                 ) -> None:
        """
        Initializes the HHParser with URL, soup class, tag name,
         and attributes.

        :param url: The URL to scrape.
        :param soup_class: The class to use for creating soup objects.
        :param tag_name: The tag name to search for in the HTML.
        :param tag_attrs: The attributes of the tag to search for.
        """
        super().__init__(url, soup_class, tag_name, tag_attrs)
        self.url: str = url
        self.soup_class: type[HHSoup] = soup_class
        self.tag_name = tag_name
        if tag_attrs is None:
            self.tag_attrs: dict[str, str] | None = {
                'data-qa': 'vacancy-serp__results'
            }

    async def start_browser(self) -> HHSoup:
        """
        Starts the browser and ensures the returned soup
         is of type HHSoup.

        :return: An instance of HHSoup containing the parsed content.
        """
        soup_instance = await super().start_browser()
        assert isinstance(soup_instance, HHSoup)
        return soup_instance

    async def parse(self) -> HHSoup:
        """
        Parses the content of the webpage for job listings.

        :return: An instance of HHSoup with parsed job offers.
        """
        soup_instance: HHSoup = await self.start_browser()
        tag = soup_instance.get_tag(self.tag_name, attrs=self.tag_attrs)
        soup_instance.parse_content(tag)
        return soup_instance

    async def parse_many(self, start: int, end: int, soup_instance: HHSoup) -> HHSoup:
        """
        Parses content from multiple offer links concurrently.

        :param start: The starting index of the offers to parse.
        :param end: The ending index (exclusive) of the offers to parse.
        :param soup_instance: The HHSoup instance containing the offer links to parse.

        :return: The updated HHSoup instance with parsed offer descriptions.
        """
        async with async_playwright() as pw:
            tasks = []
            browser = await pw.chromium.launch()
            context = await self._create_context(browser)
            async with browser:
                assert isinstance(soup_instance.offers_links, list)
                count = start
                for link in soup_instance.offers_links[start:end]:
                    page = await self._create_page(context)
                    tasks.append(self._parse_page(page, link, count, soup_instance))
                    count += 1
                await asyncio.gather(*tasks)
        return soup_instance

    async def _parse_page(self, page: Page, link: str, counter: int, current_soup: HHSoup) -> None:
        """
        Helper method to parse a single page and extract content.

        :param page: Page object from Playwright.
        :param link: URL to navigate to.
        :param counter: The index of the offer being parsed.
        :param current_soup: The HHSoup instance to update with
         parsed descriptions.

        :return: None
        :raises PWTimeoutError: If the page fails to load after maximum
         retries.
        """
        max_retries = 3
        retries = 0
        while retries < max_retries:
            try:
                await page.goto(link)
                await page.wait_for_load_state('load')
                content = await page.content()
                soup_instance = self.soup_class(content, self.parser_type)
                description = soup_instance.parse_descriptions(content)
                assert isinstance(current_soup.parsed_offers, list)
                current_soup.parsed_offers[counter].append(description)
                await page.close()
                return
            except PWTimeoutError as e:
                retries += 1
                print(f"Attempt {retries} failed: {e}. Retrying...")
                await asyncio.sleep(2 * retries)
        raise PWTimeoutError("Max retries exceeded while trying to load the page")

    async def run_parsing(self) -> HHSoup:
        """
        Runs the full parsing process, including initial parsing
         of the main page
        and subsequent concurrent parsing of individual offer pages.

        :return: An instance of HHSoup with all parsed job offers
         and their descriptions.
        """
        soup_instance = await self.parse()
        assert isinstance(soup_instance.offers_links, list)
        offers_amount: int = len(soup_instance.offers_links)
        batch_size: int = 8

        for start in range(0, offers_amount, batch_size):
            end = min(start + batch_size, offers_amount)
            await self.parse_many(start=start, end=end, soup_instance=soup_instance)

        return soup_instance
