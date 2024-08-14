#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains cache manager class."""
import json

from fastapi import status
from fastapi.responses import JSONResponse

from redis_client import redis
from .main import hh_parser


# pylint: disable=R0903
class CacheManager:
    """
    Manages caching of parsed offers using Redis.

    Provides methods to retrieve cached data from Redis or create new
    cache entries if they do not already exist.
    """

    def __init__(self) -> None:
        """
        Initializes the CacheManager with a Redis client.

        Imports the Redis client from the `main` module.
        """
        self.client = redis

    async def get_or_create(self) -> JSONResponse:
        """
        Retrieves cached parsed offers from Redis or creates a new cache
        entry.

        Checks if the cached parsed offers exist in Redis. If so, it
        decodes the cached bytes, converts them to JSON, and returns
        them in a JSONResponse. If the cache does not exist, it parses
        new data, encodes it, stores it in Redis, and returns it in a
        JSONResponse.

        :return: JSONResponse: A JSON response containing the parsed
         offers, either from the cache or newly created.
        :raises Exception: If there is an error in parsing or
         encoding/decoding the data.
        """
        if b_cache := await self.client.get('parsed_offers'):
            cache = json.loads(b_cache.decode())
            return JSONResponse(content=cache, status_code=status.HTTP_200_OK)
        soup_instance = await hh_parser()
        cache = soup_instance.parsed_offers
        b_cache = json.dumps(cache).encode()
        await self.client.set('parsed_offers', b_cache)
        return JSONResponse(content=cache, status_code=status.HTTP_201_CREATED)
