"""Description of classes related to `BeautifulSoup` management."""
from typing import Any
import re
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup, Tag, NavigableString
# pylint: disable=E0401
from exceptions import TagNotFindError


class AbstractSoup(ABC):
    """
    Abstract base class for handling content with BeautifulSoup.

    Describes the main minimal interface. Takes the key args for soup
    creating to constructor and create `BeautifulSoup` object
    using the same named method.
    We can pass any parser type for parsing processes.

    :param content: str: The HTML content to be parsed.
    :param parser_type: str: The type of parser to be used
     by BeautifulSoup (e.g., 'html.parser').
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
    def create_soup(self) -> BeautifulSoup:
        """
        Create a BeautifulSoup object from the gotten content.

        :return: BeautifulSoup: The BeautifulSoup object initialized.
        """

    @abstractmethod
    def get_tag(self, name: str, attrs: dict[str, str] | None = None,
                recursive: bool = True, **kwargs: dict[str, Any]
                ) -> Tag | NavigableString | None:
        """
        Find a tag in the BeautifulSoup object based
        on the provided criteria.

        :param name: str: The name of the tag to find.
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

    def create_soup(self) -> BeautifulSoup:
        soup: BeautifulSoup = self.beautiful_soup(self.content, self.parser_type)
        return soup

    def get_tag(self, name: str, attrs: dict[str, str] | None = None,
                recursive: bool = True, **kwargs: dict[str, Any]
                ) -> Tag | NavigableString | None:
        soup: BeautifulSoup = self.create_soup()
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
        self.offers_list: str = ''

    def parse_content(self, tag: Tag | NavigableString | None) -> None:
        if tag is None:
            raise TagNotFindError('The tag was not found. Can\'t process empty list.')
        common_offers_block: Tag | NavigableString | Any | None \
            = tag.next.next.next  # type: ignore
        self.offers_amount = int(common_offers_block.get_text().split()[0])  # type: ignore
        offers_block: Tag | NavigableString | Any | None = (common_offers_block  # type: ignore
                                                            .next_sibling
                                                            .next_sibling.next.next_sibling
                                                            .next.next.next.next.next)
        offers = (offers_block.find_all(  # type: ignore
            'div', class_=re.compile('vacancy-card--z')))
        # TODO: implement linked list instead simple list

        self.offers_list = '\n'.join(offer.get_text() for offer in offers)



    

