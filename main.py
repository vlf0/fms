#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The `main` module of app, the entrypoint."""
from typing import Annotated
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from dotenv import load_dotenv
# pylint: disable=E0401
from settings import settings

load_dotenv()
app = FastAPI()


class Task(BaseModel):
    """A class to represent a task."""

    info: str


tasks = []


@app.get('/')
async def index() -> dict[str, str]:
    """
    Endpoint to get the database URL message.

    :return: dict: A dictionary containing the message with the database URL.
    """
    return {'message': f'{settings.kis_db_url}'}


@app.post('/insert')
async def adding(task: Annotated[Task, Depends()]) -> dict[str, int]:
    """
    Endpoint to add a task to the list.

    :param task: Task: The task to be added.
    :return: dict: A dictionary containing the status code.
    """
    tasks.append(task)
    return {'status code': 200}
