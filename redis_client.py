#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contains initialized Redis client instance."""
from redis.asyncio import Redis

from settings import settings


redis: Redis = Redis.from_url(settings.redis_cache)
