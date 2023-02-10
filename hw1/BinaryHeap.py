# Binary Heap class for all your Binary needs?
import Node


class BinaryHeap:
    def __init__(self):
        self.heapList = []
        self.currentSize = 0

    def perc_up(heap_size):
        while heap_size // 2 > 0:
            if self.heapList[heap_size].f_val < self.heapList[heap_size // 2].f_val:
                tmp = self.heapList[heap_size // 2]
                self.heapList[heap_size // 2] = self.heapList[heap_size]
                self.heapList[heap_size] = tmp
            heap_size = heap_size // 2

    def insert(n):
        self.heapList.append(n)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)
