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

  This function is used for pagination. It takes the page number (1-indexed)
  and the desired number of items per page as arguments. It returns a tuple
  containing the starting index and the ending index (exclusive) for the data
  to be retrieved for that specific page.

  Args:
      page (int): The page number to retrieve (starting from 1).
      page_size (int): The number of items to include per page.

  Returns:
      tuple: A tuple containing the starting and ending index for the data.
  """
  start_index = 0
  end_index = 0

  # Calculate the starting and ending index based on page and page size
  for _ in range(page):
    start_index = end_index
    end_index += page_size

  return start_index, end_index


class Server:
  """
  Server class for paginating a database of popular baby names stored in a CSV file.

  This class provides methods to access and manage the baby names data. It can
  retrieve specific pages of data based on user-provided page number and page size.
  """
  DATA_FILE = "Popular_Baby_Names.csv"

  def __init__(self):
    """
    Initializes the server object.

    This constructor doesn't take any arguments. It initializes an internal attribute
    to store the loaded baby names data (`self.__dataset`). This attribute is set
    to `None` initially.
    """
    self.__dataset = None

  def dataset(self) -> List[List]:
    """
    Loads and caches the baby names data from the CSV file.

    This method retrieves the baby names data from the specified CSV file
    (stored in the `DATA_FILE` attribute). It uses a cache to avoid re-reading
    the file on every call. The data is stored as a list of lists, where each inner
    list represents a single record (baby name entry) from the CSV file.

    Returns:
        list: A list of lists containing the baby names data loaded from the CSV file.
    """
    if self.__dataset is None:
      with open(self.DATA_FILE) as f:
        reader = csv.reader(f)
        # Skip the header row
        next(reader)  # Assuming the first row contains headers
        dataset = [row for row in reader]
      self.__dataset = dataset

    return self.__dataset

  def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
    """
    Retrieves a specific page of baby names data.

    This method takes the desired page number (defaulting to 1) and the number of
    items per page (defaulting to 10) as arguments. It retrieves the corresponding
    data from the loaded baby names dataset and returns it as a list of lists.

    Args:
        page (int, optional): The page number to retrieve (default: 1).
        page_size (int, optional): The number of items per page (default: 10).

    Returns:
        list: A list of lists containing the baby names data for the requested page.

    Raises:
        AssertionError: If either page or page_size is not a positive integer.
        IndexError: If the requested page is beyond the available data.
    """
    # Validate input arguments (page and page_size must be positive integers)
    assert isinstance(page, int) and page > 0
    assert isinstance(page_size, int) and page_size > 0

    dataset = self.dataset()
    data_length = len(dataset)

    try:
      # Calculate start and end index for the requested page
      start_index, end_index = index_range(page, page_size)
      # Return the data slice for the requested page
      return dataset[start_index:

