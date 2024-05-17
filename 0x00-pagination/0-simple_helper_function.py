#!/usr/bin/env python3
"""
index_range helper function
"""
from typing import Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    returns a tuple of size two containing start stop index corresponding
    to the range
    Args:
        page (int): page number
        page_size (int): item amount per page
    Return:
        tuple
    """
    start, end = 0, 0
    for i in range(page):
        start = end
        end += page_size

    return (start, end)
