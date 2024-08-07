#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to starting parsers."""
from fastapi import status
from fastapi.responses import JSONResponse
# pylint: disable=E0401
# pylint: disable=W4901
from web_parser import HHParser, HH_URL, HHSoup


async def hh_parser() -> JSONResponse:
    """Start parser working and return parsed data as the response."""
    parser: HHParser = HHParser(HH_URL, HHSoup)
    soup_instance: HHSoup = await parser.parse_many()
    response: JSONResponse = JSONResponse(content=soup_instance.parsed_offers,
                                          status_code=status.HTTP_200_OK)
    return response
