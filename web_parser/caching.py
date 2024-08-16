#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains cache manager class."""
import json

from fastapi import status
from fastapi.responses import JSONResponse

from celery_app import run_parser_task
from redis_client import redis


# pylint: disable=R0903
class CacheManager:
    """
    Manages caching of parsed offers using Redis.

    This class provides methods to retrieve cached data from Redis or
    to create new cache entries if they do not already exist.
    """

    def __init__(self) -> None:
        """
        Initializes the CacheManager with a Redis client.

        :return: None
        """
        self.client = redis

    async def get_or_create(self) -> dict[str, str]:
        """
        Retrieves cached data or initiates a Celery task to create it.

        :return: Cached data as a string if it exists, otherwise
         a dictionary indicating the task has been launched.
        """
        if b_cache := await self.client.get('parsed_offers'):
            cache: str = json.loads(b_cache.decode())
            return {'parsed_data': cache}
        run_parser_task.delay()
        return {'parsed_data': 'in process'}

    async def response_result(self) -> JSONResponse:
        """
        Returns a JSON response with either cached data or task status.

        :return: A JSON response with a 304 Not Modified status if the
         cached data is available, or a 200 OK status with task
         information if the data is being generated.
        """
        content = await self.get_or_create()
        if isinstance(content, str):
            code = status.HTTP_304_NOT_MODIFIED
        else:
            code = status.HTTP_200_OK
        return JSONResponse(content=content, status_code=code)
