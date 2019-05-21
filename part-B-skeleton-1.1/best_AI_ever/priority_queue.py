"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

import heapq

class PriorityQueue:
    """
    PriorityQueue implemented using heapq.
    Reference: https://segmentfault.com/a/1190000010007858
    """
    def __init__(self):
        """
        Initialise the PriorityQueue by assigning 0 to index and size, and an
        empty list to queue.
        """
        self._index = 0
        self._queue = []
        self.size = 0

    def push(self, item, priority):
        """
        Push an item into the priority queue with the specified priority.
        """
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        self.size += 1

    def pop(self):
        """
        Pop an item with the smallest priority from the queue.
        """
        self.size -= 1
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        """
        Check if the priority queue is empty.
        """
        return self.size == 0
