#!/usr/bin/python3
""" FIFOCache module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache defines a FIFO caching system
    """

    def __init__(self):
        """ Initialize the class
        """
        super().__init__()
        self.order = []  # List to maintain the order of keys for FIFO

    def put(self, key, item):
        """ Add an item in the cache using FIFO algorithm
        """
        if key is None or item is None:
            return

        if key not in self.cache_data and len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            first_key = self.order.pop(0)  # Remove the first key added (FIFO)
            del self.cache_data[first_key]  # Remove it from cache
            print(f"DISCARD: {first_key}")

        self.cache_data[key] = item
        if key not in self.order:
            self.order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        return self.cache_data.get(key, None)
