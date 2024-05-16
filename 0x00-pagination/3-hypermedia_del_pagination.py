#!/usr/bin/env python3
"""
Provides a server class for paginating baby name data with deletion resilience.

This script defines a `Server` class for managing and retrieving paginated baby 
names data loaded from a CSV file. It prioritizes resilience against potential 
deletions in the original data source.

The class offers functionalities for:

- Data loading and caching: Loads the baby names data from a CSV file and stores 
  it internally for efficient retrieval.
- Indexed dataset creation (cached): Generates a dictionary where keys are the 
  original positions (0-based indexing) of baby name entries in the complete 
  data and values are the corresponding records. This indexing facilitates 
  skipping over potentially deleted entries during pagination.
- Hypermedia pagination with deletion resilience: Retrieves a specific page of 
  baby names data while considering potential deletions. It iterates through 
  requested page size, fetching entries at calculated positions and skipping 
  over missing entries (using `dataset.get`) to maintain pagination consistency.

The `indexed_dataset` is limited to the first 1000 entries by default, potentially 
limiting resilience for deletions beyond that point. 
"""

import csv
import math
from typing import List, Dict


class Server:
    """
    Server class for paginating a database of popular baby names stored in a CSV file, 
    focusing on resilience against potential deletions in the original data.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        """
        Initializes the server object.

        This constructor doesn't take any arguments. It initializes two internal 
        attributes:

        - `__dataset`: Stores the loaded baby names data as a list of lists 
          (not used in `get_hyper_index`).
        - `__indexed_dataset`: Stores the baby names data indexed by their 
          original positions in the file (0-based indexing) for deletion 
          resilience.
        """
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """
        Loads and caches the baby names data from the CSV file.

        This method retrieves the baby names data from the specified CSV file 
        (stored in the `DATA_FILE` attribute). It uses a cache to avoid re-reading 
        the file on every call. The data is stored as a list of lists, where each 
        inner list represents a single baby name entry from the CSV file.

        Returns:
            list: A list of lists containing the baby names data loaded from the CSV file.
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """
        Creates and caches an indexed dataset for deletion-resilient pagination.

        This method generates a dictionary for efficient access to baby name 
        entries based on their original positions in the complete data. It's 
        called if the `__indexed_dataset` attribute is not yet set.

        Steps:

        1. Calls `dataset` to retrieve the complete baby names data.
        2. Creates a truncated copy of the data containing the first 1000 entries 
           (for potential deletion resilience). This truncation is a trade-off 
           between memory usage and resilience for deletions beyond the 1000th 
           entry.
        3. Constructs a dictionary where keys are the original positions (0-based 
           indexing) of entries in the complete data and values are the 
           corresponding baby name records.

        Returns:
            dict: A dictionary with baby name entries indexed by their original 
                  positions for deletion-resilient pagination.
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict:
        """
        Retrieves a page of baby names data with deletion resilience.

        This method extracts a page of data starting from the provided index, 
        ensuring it skips over any deleted entries. It returns a dictionary 
        containing the page of data along with hypermedia pagination details.

        Args:
            index (int, optional): The starting index for the page (default: None).
            page_size (int, optional): The number of items per page (default: 10).

        Returns:
            dict: A dictionary containing the page data and pagination details:
                  - index: The current start index.
                  - next_index: The starting index for the next page.
                  - page_size: The current page size.
                  - data: The list of baby names data for the current page.
        """
        indexed_data = self.indexed_dataset()
        data = []
        current_index = index if index is not None else 0

        while len(data) < page_size and current_index < len(indexed_data):
            record = indexed_data.get(current_index)
            if record is not None:
                data.append(record)
            current_index += 1

        next_index = current_index if current_index < len(indexed_data) else None

        return {
            "index": index,
            "next_index": next_index,
            "page_size": len(data),
            "data": data
        }
