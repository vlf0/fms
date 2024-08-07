#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description of classes related to `BeautifulSoup` management."""
from typing import Any
import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag, NavigableString
from fms.exceptions import TagNotFindError  # type: ignore


class AbstractSoup(ABC):
    """
    Abstract base class for handling content with BeautifulSoup.

    Describes the main minimal interface. Takes the key args for soup
    creating to constructor and create `BeautifulSoup` object
    using the same named method.
    We can pass any parser type for parsing processes.
    """

    def __init__(self, content: str, parser_type: str) -> None:
        """
        Initializes the AbstractSoup with content and parser type.

        :param content: str: The HTML content to be parsed.
        :param parser_type: str: The parser type to use
         with BeautifulSoup.
        """
        super().__init__()
        self.beautiful_soup: type[BeautifulSoup] = BeautifulSoup
        self.content: str = content
        self.parser_type: str = parser_type

    @abstractmethod
    def create_soup(self, content: str) -> BeautifulSoup:
        """
        Create a BeautifulSoup object from the gotten content.

        :return: BeautifulSoup: The BeautifulSoup object initialized.
        """

    @abstractmethod
    def get_tag(self, name: str, content: str | None = None,
                attrs: dict[str, str] | None = None,
                recursive: bool = True, **kwargs: dict[str, Any]
                ) -> Tag | NavigableString | None:
        """
        Find a tag in the BeautifulSoup object based
        on the provided criteria.

        :param name: str: The name of the tag to find.
        :param content: str: The content of the defined page to parsing.
        :param attrs: dict[str, str] | None: A dictionary of attributes
         to filter the tag.
        :param recursive: bool: Whether to search recursively.
        :param kwargs: Additional arguments passed
         to BeautifulSoup's find method.
        :return: Tag | NavigableString | None: The found tag,
         NavigableString, or None if not found.
        """

    @abstractmethod
    def parse_content(self, tag: Tag | NavigableString | None) -> None:
        """
        Parse the content of the provided tag and extract information.

        :param tag: Tag: The tag whose content needs to be parsed.
        :return: list[Tag | None]: A list of tags or None
         extracted from the content.
        """


class BaseSoup(AbstractSoup):
    """
    A base class realizing interfaces of `AbstractSoup` that provides
    basic functionality for parsing.

    :param content: str: The content to be parsed.
    :param parser_type: str: The type of parser to be used
     by BeautifulSoup.
    """

    def create_soup(self, content: str) -> BeautifulSoup:
        soup: BeautifulSoup = self.beautiful_soup(content, self.parser_type)
        return soup

    def get_tag(self, name: str, content: str | None = None,
                attrs: dict[str, str] | None = None,
                recursive: bool = True, **kwargs: dict[str, Any]
                ) -> Tag | NavigableString | None:
        content = content if content is not None else self.content
        soup: BeautifulSoup = self.create_soup(content)
        tag: Tag | NavigableString | None = (
            soup.find(name, attrs=attrs)) if attrs else soup.find(name)
        return tag

    def parse_content(self, tag: Tag | NavigableString | None) -> None:
        raise NotImplementedError("Subclasses should implement this method")


class HHSoup(BaseSoup):
    """
    A concrete implementation of BaseSoup for handling specific content.

    :param content: str: The content to be parsed.
    :param parser_type: str: The type of parser to be used by BeautifulSoup.
    """

    def __init__(self, content: str, parser_type: str):
        super().__init__(content, parser_type)
        self.offers_amount: int = 0
        self.offers_links: list[str] | None = None
        self.offers_list: list[Tag] | None = None
        self.parsed_offers: list[tuple[str, ...]] | None = None
        self.descriptions: list[str] | None = None

    def parse_content(self, tag: Tag | NavigableString | None) -> None:
        if tag is None:
            raise TagNotFindError('The tag was not found. Can\'t process empty list.')
        self.offers_list = tag.find_all('div',  # type: ignore
                                        attrs={'class': re.compile('vacancy-card--z')})
        self.parsed_offers = []
        self.offers_links = []
        self.split_parse_content()

    def split_parse_content(self) -> None:
        """
        Splits and parses the content of each job offer.

        This method iterates over the list of job offers (`self.offers_list`),
        extracting relevant details such as name, link, salary, experience,
        remote status, and company. The parsed details are stored in
        `self.parsed_offers`, and the offer links are stored in `self.offers_links`.

        :raises AttributeError: If an attribute is not found during parsing.
        :raises TypeError: If an unexpected type is encountered during parsing.
        """
        for offer in self.offers_list:  # type: ignore
            header = offer.find('h2')
            name = header.text  # type: ignore
            link = header.find('a').attrs.get('href')  # type: ignore
            data = offer.find('div', class_=re.compile('compensation-labels--'))
            next_element = data.next  # type: ignore

            if next_element.name == 'div':  # type: ignore
                salary = None
                exp = next_element
            else:
                salary = (next_element.text.replace('\u202f', ' ')  # type: ignore
                          .replace('\xa0', ' '))
                exp = next_element.next_sibling  # type: ignore
            remote = exp.next_sibling  # type: ignore
            company = offer.find('span', class_=re.compile('company-info-text--'))
            if company is None:
                company = offer.find('a', attrs={'data-qa': re.compile('vacancy-serp_')})
            company = company.text.replace('\xa0', ' ')  # type: ignore
            try:
                self.parsed_offers.append((name, salary, exp.text, remote.text,  # type: ignore
                                           company, link))
            except (AttributeError, TypeError):
                pass
            self.offers_links.append(link)  # type: ignore

    def parse_descriptions(self, extra_content: str) -> None:
        """
        Parses job descriptions from additional content.

        This method extracts and processes job descriptions from the
        given `extra_content`. The descriptions are appended to
        `self.descriptions`.

        :param extra_content: str: The HTML content containing additional job details.
        """
        self.descriptions = []
        text_block = self.get_tag('div', content=extra_content,
                                  attrs={'class': 'vacancy-description'})
        description_full = text_block.text  # type: ignore
        description_part = description_full.split('Задайте')[0]
        single_line_text = ' '.join(description_part.split())
        self.descriptions.append(single_line_text)
