#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to starting parsers."""
from fastapi import status
from fastapi.responses import JSONResponse

from web_parser import HHParser, HH_URL, HHSoup


async def hh_parser() -> JSONResponse:
    """Start parser working and return parsed data as the response."""
    parser: HHParser = HHParser(HH_URL, HHSoup)
    soup_instance: HHSoup = await parser.run_parsing()
    response: JSONResponse = JSONResponse(content=soup_instance.parsed_offers,
                                          status_code=status.HTTP_200_OK)
    return response
