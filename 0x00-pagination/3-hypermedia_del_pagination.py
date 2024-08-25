#!/usr/bin/env python3
"""
implement the get_hyper_index method in the Server class that handles
deletion-resilient pagination.
"""
import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset"""
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0"""
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = None, page_size: int = 10) -> Dict[str, Any]:
        """
        Get the dataset page along with information for hypermedia pagination.

        Args:
            index (int): The start index of the page.
            page_size (int): The number of items per page.

        Returns:
            Dict[str, Any]: A dictionary containing the start index, the data, the page size, and the next index.
        """
        assert index is not None and 0 <= index < len(self.indexed_dataset()), "Index out of range."

        dataset = self.indexed_dataset()
        data = []
        current_index = index
        count = 0

        # Collect the data while handling deletions
        while count < page_size and current_index < len(dataset):
            if current_index in dataset:
                data.append(dataset[current_index])
                count += 1
            current_index += 1

        next_index = current_index if current_index < len(dataset) else None

        return {
            'index': index,
            'data': data,
            'page_size': len(data),
            'next_index': next_index
        }


# Example usage (from your 3-main.py script):
if __name__ == "__main__":
    server = Server()
    server.indexed_dataset()

    try:
        server.get_hyper_index(300000, 100)
    except AssertionError:
        print("AssertionError raised when out of range")

    index = 3
    page_size = 2

    print("Nb items:", len(server._Server__indexed_dataset))

    # 1- request first index
    res = server.get_hyper_index(index, page_size)
    print(res)

    # 2- request next index
    print(server.get_hyper_index(res.get('next_index'), page_size))

    # 3- remove the first index
    del server._Server__indexed_dataset[res.get('index')]
    print("Nb items:", len(server._Server__indexed_dataset))

    # 4- request again the initial index -> the first data retrieved is not the same as the first request
    print(server.get_hyper_index(index, page_size))

    # 5- request again initial next index -> same data page as the request 2-
    print(server.get_hyper_index(res.get('next_index'), page_size))

