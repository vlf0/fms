#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description of custom exceptions."""


class TagNotFindError(Exception):
    """
    Exception raised when a tag is not found during parsing.

    This custom exception is used to signal that a specific tag
    was expected but not found in the content being parsed.
    """

    def __init__(self, message: str) -> None:
        """
        Initializes the TagNotFindError with a message.

        :param message: str: The message describing the error.
        """
        super().__init__(message)
        self.message: str = message

    def __str__(self) -> str:
        """
        Returns a string representation of the TagNotFindError.

        :return: str: A formatted string including the class name and message.
        """
        return f'Was caught {self.__class__.__name__}! {self.message}'
