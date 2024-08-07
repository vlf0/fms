#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The `main` module of app, the entrypoint."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
# pylint: disable=E0401
# pylint: disable=C0411
from auth.endpoints import router as auth_router
from web_parser.endpoints import router as parser_router

load_dotenv()

app = FastAPI()
app.include_router(auth_router)
app.include_router(parser_router)

# origins = [
#     'http://localhost:3000',
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=['GET', 'HEAD', 'OPTIONS', 'POST'],
#     allow_headers=['Content-Type', 'Access-Control-Allow-Origin'],
#     allow_credentials=True
# )


origins = [
    'http://localhost',
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    # allow_headers=['Cookie'],
)



# @router.post('/main')
# async def index() -> JSONResponse:
#     return
