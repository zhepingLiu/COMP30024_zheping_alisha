"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

import heapq

class PriorityQueue:
    def __init__(self):
        self._index = 0
        self._queue = []
        self.size = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        self.size += 1

    def pop(self):
        self.size -= 1
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return self.size == 0