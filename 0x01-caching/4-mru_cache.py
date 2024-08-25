#!/usr/bin/env python3
""" MRUCache module
"""
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """ MRUCache defines a MRU caching system
    """

    def __init__(self):
        """ Initialize the class
        """
        super().__init__()
        self.access_order = []  # List to keep track of the order of access

    def put(self, key, item):
        """ Add an item in the cache using MRU algorithm
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # If the key is already in the cache, remove it from its current position
            self.access_order.remove(key)
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            # If the cache is full, remove the most recently used item
            mru_key = self.access_order.pop()
            del self.cache_data[mru_key]
            print(f"DISCARD: {mru_key}")

        # Add the new key-value pair and update the access order
        self.cache_data[key] = item
        self.access_order.append(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Move the accessed key to the end to show it was recently used
        self.access_order.remove(key)
        self.access_order.append(key)
        return self.cache_data[key]
