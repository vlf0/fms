#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The `main` module of app, the entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.endpoints import router as auth_router
from web_parser.endpoints import router as parser_router


app: FastAPI = FastAPI()
app.include_router(auth_router)
app.include_router(parser_router)

origins: list[str] = [
    'http://localhost:3000',
    'http://159.65.135.38:30'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST']
)
