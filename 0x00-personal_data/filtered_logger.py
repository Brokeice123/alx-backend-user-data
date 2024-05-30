#!/usr/bin/env python3
"""
Module that uses regex to replace occurrences of certain
fields
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Function that replaces occurrences of certain fields
    with redaction
    """
    for f in fields:
        message = re.sub(f + "=.*?" + separator,
                         f + "=" + redaction + separator, message)

    return message
