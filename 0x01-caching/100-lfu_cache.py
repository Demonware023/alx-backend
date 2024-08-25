#!/usr/bin/env python3
""" LFUCache module
"""
from base_caching import BaseCaching
from collections import OrderedDict


class LFUCache(BaseCaching):
    """ LFUCache defines an LFU caching system
    """

    def __init__(self):
        """ Initialize the class
        """
        super().__init__()
        self.key_freq = {}  # Dictionary to store the frequency of each key
        self.key_order = OrderedDict()  # Ordered dictionary to maintain the order of usage

    def put(self, key, item):
        """ Add an item in the cache using LFU algorithm
        """
        if key is None or item is None:
            return

        if key in self.cache_data:
            # Update item and frequency
            self.cache_data[key] = item
            self.key_freq[key] += 1
            self.key_order.move_to_end(key)
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find the least frequently used items
                min_freq = min(self.key_freq.values())
                least_freq_items = [k for k, v in self.key_freq.items() if v == min_freq]

                if len(least_freq_items) > 1:
                    # Apply LRU strategy among the least frequently used items
                    lru_key = min(least_freq_items, key=lambda k: self.key_order[k])
                else:
                    lru_key = least_freq_items[0]

                # Remove the item from cache and key_freq
                del self.cache_data[lru_key]
                del self.key_freq[lru_key]
                self.key_order.pop(lru_key)
                print(f"DISCARD: {lru_key}")

            # Add the new item
            self.cache_data[key] = item
            self.key_freq[key] = 1
            self.key_order[key] = None  # Add to order; value is not used
            self.key_order.move_to_end(key)

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        # Update frequency and order
        self.key_freq[key] += 1
        self.key_order.move_to_end(key)
        return self.cache_data[key]
