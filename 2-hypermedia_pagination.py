#!/usr/bin/env python3
"""
Provides a Server class for paginating baby name data from a CSV file.

This script defines a `Server` class that can be used to retrieve paginated
results from a database of popular baby names stored in a CSV file. It offers
methods to:
  - Load the baby names data from the CSV file.
  - Validate user-provided page and page size arguments.
  - Retrieve a specific page of baby names data based on page number and page size.
  - Generate a hypermedia representation of a requested page, including
    - page number
    - page size (adjusted to actual data size if necessary)
    - total number of pages
    - data for the requested page
    - links to previous and next pages (if applicable)
"""

import csv
from typing import List

# Import the index_range function from another module (assumed to be in the same directory)
index_range = __import__('0-simple_helper_function').index_range


class Server:
    """
    Server class for paginating a database of popular baby names stored in a CSV file.

    This class provides functionalities for managing and retrieving paginated baby
    names data.
    """

    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initializes the server object.

        This constructor doesn't take any arguments. It initializes an internal
        attribute (`self.__dataset`) to store the loaded baby names data as a list
        of lists (where each inner list represents a single baby name entry).
        The data is initially set to `None`.
        """
        self.__dataset = None

    def dataset(self) -> List[List]:
        """
        Loads the baby names data from the CSV file and returns it as a list of lists.

        This method retrieves the baby names data from the specified CSV file
        stored in the `DATA_FILE` attribute. It uses a cache (`self.__dataset`) to
        avoid re-reading the file on every call.

        Returns:
            List[List]: The baby names data loaded from the CSV file.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                # Skip the header row (assuming the first row contains headers)
                next(reader)
                dataset = [row for row in reader]
            self.__dataset = dataset

        return self.__dataset

    @staticmethod
    def assert_positive_integer_type(value: int) -> None:
        """
        Raises an AssertionError if the provided value is not a positive integer.

        This static method validates that the provided `value` is a positive
        integer. It raises an `AssertionError` if the validation fails.

        Args:
            value (int): The value to be validated.
        """
        assert type(value) is int and value > 0

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """
        Retrieves a specific page of baby names data based on page number and page size.

        This method takes the desired page number (defaulting to 1) and the number of
        items per page (defaulting to 10) as arguments. It validates the arguments
        and retrieves the corresponding data from the loaded baby names dataset. If
        the requested page is beyond the available data, an empty list is returned.

        Args:
            page (int, optional): The page number to retrieve (default: 1).
            page_size (int, optional): The number of items per page (default: 10).

        Returns:
            List[List]: A list of lists containing the baby names data for the
                         requested page, or an empty list if the page is out of bounds.
        """
        self.assert_positive_integer_type(page)
        self.assert_positive_integer_type(page_size)
        dataset = self.dataset()
        start, end = index_range(page, page_size)
        try:
            # Return the data slice for the requested page
            return dataset[start:end]
        except IndexError:
            return []

    def get_hyper(self, page: int = 1, page_size: int = 10) -> dict:
        """
        Returns a hyper
        """
        total_pages = len(self.dataset()) // page_size + 1
        data = self.get_page(page, page_size)
        info = {
            "page": page,
            "page_size": page_size if page_size <= len(data) else len(data),
            "total_pages": total_pages,
            "data": data,
            "prev_page": page - 1 if page > 1 else None,
            "next_page": page + 1 if page + 1 <= total_pages else None
        }
        return info
