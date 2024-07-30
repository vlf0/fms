#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains async iterable classes."""


class AsyncList:
    """
    Asynchronous iterator for a list of strings.

    This class provides asynchronous iteration over a list of strings.
    It implements the asynchronous iteration protocol, allowing it to
    be used with `async for` loops.

    :param sequence: list[str]: The list of strings to iterate over.
    """

    def __init__(self, sequence: list[str]) -> None:
        """
        Initializes the AsyncList with a list of strings.

        :param sequence: list[str]: The list of strings to be iterated.
        """
        self.sequence: list[str] = sequence
        self.index: int = 0

    def __aiter__(self) -> 'AsyncList':
        """
        Returns the asynchronous iterator object.

        :return: AsyncList: The AsyncList instance itself.
        """
        return self

    async def __anext__(self) -> str:
        """
        Returns the next string in the sequence asynchronously.

        If there are no more items in the sequence, raises StopAsyncIteration.

        :return: str: The next string in the sequence.
        :raises StopAsyncIteration: If there are no more items to return.
        """
        if self.index >= len(self.sequence):
            raise StopAsyncIteration
        item: str = self.sequence[self.index]
        self.index += 1
        return item
