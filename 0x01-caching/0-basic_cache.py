#!/usr/bin/env python3
"""
Basecache thing
"""
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """
    caching information in key-value
    """

    def __init__(self):
        """
        initialization of basecache
        """
        BaseCaching.__init__(self)

    def put(self, key, item):
        """
        assign to the dictionary
        """
        if key is None or item is None:
            pass
        else:
            self.cache_data[key] = item

    def get(self, key):
        """
        value linked to the key/nothing
        """
        if key is not None and key in self.cache_data.keys():
            return self.cache_data[key]
        return None
