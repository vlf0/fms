#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to starting parsers."""
from web_parser import HHParser, HH_URL, HHSoup


async def hh_parser() -> HHSoup:
    """
    Start parser working and return filled with parsed data
    soup instance.
    """
    parser: HHParser = HHParser(HH_URL, HHSoup)
    soup_instance: HHSoup = await parser.parse()
    return soup_instance
