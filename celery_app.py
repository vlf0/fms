#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Description instantiated Celery app tasks and task manager."""
import json

import asyncio
from celery import Celery, Task
from celery.result import AsyncResult

from redis_client import redis
from settings import settings
from web_parser import HHSoup
from web_parser.main import hh_parser


celery_app = Celery(
    main='celery_app',
    broker=settings.celery_broker,
    backend=settings.celery_backend
)
celery_app.conf.update(
    task_result_expires=3600
)


# pylint: disable=W0613
@celery_app.task(name='run_parser_task')  # type: ignore
def run_parser_task(*args, **kwargs) -> None:
    """
    Executes the web parser task and stores the parsed offers in Redis.

    :param args: Positional arguments for the task.
    :param kwargs: Keyword arguments for the task.
    :return: None
    """
    parsed_result: HHSoup = start_parsing_sync()
    b_cache: bytes = json.dumps(parsed_result.parsed_offers).encode()
    asyncio.run(redis.set('parsed_offers', b_cache, ex=1800))


def start_parsing_sync() -> HHSoup:
    """
    Retrieves or creates parsed data synchronously.

    :return: A string representing the parsed data.
    """
    return asyncio.run(hh_parser())


# pylint: disable=R0903
class TasksManager:
    """Class to manage statuses and results of celery tasks."""

    def __init__(self, task: Task) -> None:
        """
        Initializes the TasksManager with the given task.

        :param task: The Celery task to manage.
        """
        self.task = task

    async def get_result(self, interval: int) -> None:
        """
        Polls the Celery task result at regular intervals.

        :param interval: Time interval (in seconds) between polling attempts.
        :return: A string indicating the task result status.
        :raises Exception: If the task fails or does not complete.
        """
        async_result = AsyncResult(self.task.id, app=celery_app)

        while not async_result.ready():
            await asyncio.sleep(interval)

        if async_result.state == 'SUCCESS':
            # logger.info(async_result.result)
            # TODO: implement sending via websocket when ready
            ...
        elif async_result.state == 'FAILURE':
            raise Exception("Task failed")
        else:
            raise Exception("Task did not complete")
