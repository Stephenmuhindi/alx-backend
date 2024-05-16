#!/usr/bin/env python3
"""
This script defines a Server class that can be used to paginate a database
of popular baby names stored in a CSV file.

Pagination allows for retrieving data in smaller, more manageable chunks. 
This server class provides methods to access specific pages of the baby names data.
"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """
    Calculates the start and end index for a given page and page size.

    Args:
        page (int): The page number to retrieve (starting from 1).
        page_size (int): The number of items to include per page.

    Returns:
        tuple: A tuple containing the starting and ending index for the data.
    """
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """
    Server class for paginating a database of popular baby names stored in a CSV file.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initializes the server object.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the baby names data from the CSV file.

        Returns:
            list: A list of lists containing the baby names data loaded from the CSV file.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                # Skip the header row
                next(reader)
                self.__dataset = [row for row in reader]
        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of baby names data.

        Args:
            page (int, optional): The page number to retrieve (default: 1).
            page_size (int, optional): The number of items per page (default: 10).

        Returns:
            list: A list of lists containing the baby names data for the requested page.

        Raises:
            AssertionError: If either page or page_size is not a positive integer.
            IndexError: If the requested page is beyond the available data.
        """
        # Validate input arguments
        assert isinstance(page, int) and page > 0, "Page must be a positive integer."
        assert isinstance(page_size, int) and page_size > 0, "Page size must be a positive integer."

        dataset = self.dataset()
        start_index, end_index = index_range(page, page_size)

        if start_index >= len(dataset):
            return []

        return dataset[start_index:end_index]
