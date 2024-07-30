#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to starting parsers."""
from typing import cast
import asyncio
# pylint: disable=E0401
# pylint: disable=W4901
from parser import HHParser, HH_URL, HHSoup

# Create an instance of HHParser
parser: HHParser = HHParser(HH_URL, HHSoup)

# Run the parser to get processed instance
processed_instance = asyncio.run(parser.parse())

# Get the list of offers
offers = processed_instance.parsed_offers
offers = cast(list[tuple[str, ...]], offers)

# Print each offer
for i in offers:
    print(i)
