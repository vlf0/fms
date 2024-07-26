"""Description of parsers classes."""
import random
from abc import ABC, abstractmethod
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page
)
from bs4 import Tag
from fms.parser.soups import HHSoup, BaseSoup

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


class AbstractParser(ABC):

    def __init__(self, url: str, user_agents: tuple[str, ...]) -> None:
        super().__init__()
        self.url: str = url
        self.user_agents: tuple[str, ...] = user_agents
        self.parser_type = 'html.parser'

    @abstractmethod
    async def _create_page(self, browser: Browser) -> Page:
        pass

    @abstractmethod
    async def parse(self, content: str) -> list[Tag | None]:
        pass

    @abstractmethod
    async def start_browser(self) -> list[Tag | None]:
        pass


class BaseParser(AbstractParser):

    def __init__(self, url: str,
                 soup_class: type[BaseSoup] = BaseSoup,
                 tag_name: str = 'default',
                 tag_attrs: dict[str, str] | None = None,
                 user_agents: tuple[str, ...] = USER_AGENTS,
                 ) -> None:
        super().__init__(url, user_agents)
        self.url: str = url
        self.user_agents: tuple[str, ...] = user_agents
        self.soup_class: type[BaseSoup] = soup_class
        self.tag_name: str = tag_name
        self.tag_attrs: dict[str, str] | None = tag_attrs

    async def _create_page(self, browser: Browser) -> Page:
        user_agent: str = random.choice(self.user_agents)
        context: BrowserContext = await browser.new_context(user_agent=user_agent)
        page: Page = await context.new_page()
        return page

    async def parse(self, content: str) -> list[Tag | None]:

        soup_class: BaseSoup = self.soup_class(content, self.parser_type)
        tag = soup_class.get_tag(self.tag_name, attrs=self.tag_attrs)
        parsed_data: list[Tag | None] = soup_class.parse_content(tag)
        return parsed_data

    async def start_browser(self) -> list[Tag | None]:
        async with async_playwright() as pw:
            browser: Browser = await pw.chromium.launch(headless=False)
            async with browser:
                page: Page = await self._create_page(browser)
                async with page as p:
                    await p.goto(self.url)
                    await p.wait_for_load_state()
                    content = await p.content()
                    result: list[Tag | None] = await self.parse(content)
                    return result


class HHParser(BaseParser):

    def __init__(self,
                 url: str,
                 soup_class: type[BaseSoup] = HHSoup,
                 tag_name: str = 'div',
                 tag_attrs: dict[str, str] | None = None
                 ) -> None:
        super().__init__(url, soup_class, tag_name, tag_attrs)
        self.url: str = url
        self.soup_class = soup_class
        self.tag_name = tag_name
        if tag_attrs is None:
            self.tag_attrs: dict[str, str] | None = {
                'class': 'HH-MainContent HH-Supernova-MainContent'
            }
