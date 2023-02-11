# Binary Heap class for all your Binary needs?
from Node import Node


class BinaryHeap:
    def __init__(self):

        self.heap_list = [0]
        self.current_size = 0

    def sift_up(self, i):

        # While the element is not the root or the left element
        Stop = False
        while (i // 2 > 0) and Stop == False:
            # If the element is less than its parent swap the elements
            if self.heap_list[i].f_val < self.heap_list[i // 2].f_val:
                self.heap_list[i].f_val, self.heap_list[i //
                                                        2].f_val = self.heap_list[i // 2].f_val, self.heap_list[i].f_val
            else:
                Stop = True
            # Move the index to the parent to keep the properties
            i = i // 2

    def insert(self, k):

        # Append the element to the heap
        self.heap_list.append(k)
        # Increase the size of the heap.
        self.current_size += 1
        # Move the element to its position from bottom to the top
        self.sift_up(self.current_size)

    def sift_down(self, i):
        # if the current node has at least one child
        while (i * 2) <= self.current_size:
            # Get the index of the min child of the current node
            mc = self.min_child(i)
            # Swap the values of the current element is greater than its min child
            if self.heap_list[i].f_val > self.heap_list[mc].f_val:
                self.heap_list[i].f_val, self.heap_list[mc].f_val = self.heap_list[mc].f_val, self.heap_list[i].f_val
            i = mc

    def min_child(self, i):
        # If the current node has only one child, return the index of the unique child
        if (i * 2)+1 > self.current_size:
            return i * 2
        else:
            # Herein the current node has two children
            # Return the index of the min child according to their values
            if self.heap_list[i*2].f_val < self.heap_list[(i*2)+1].f_val:
                return i * 2
            else:
                return (i * 2) + 1

    def delete_min(self):
        # Equal to 1 since the heap list was initialized with a value
        if len(self.heap_list) == 1:
            return 'Empty heap'

        # Get root of the heap (The min value of the heap)
        root = self.heap_list[1]

        # Move the last value of the heap to the root
        self.heap_list[1] = self.heap_list[self.current_size]

        # Pop the last value since a copy was set on the root
        *self.heap_list, _ = self.heap_list

        # Decrease the size of the heap
        self.current_size -= 1

        # Move down the root (value at index 1) to keep the heap property
        self.sift_down(1)

        # Return the min value of the heap
        return root


if __name__ == "__main__":
    bh = BinaryHeap()
    n = Node()
    n.f_val = 9
    m = Node()
    m.f_val = 6
    p = Node()
    p.f_val = 5
    l = Node()
    l.f_val = 1
    r = Node()
    r.f_val = 3
    bh.insert(n)
    bh.insert(m)
    bh.insert(p)
    bh.insert(l)
    bh.insert(r)
    print(bh.delete_min().f_val)
    print(bh.delete_min().f_val)
    w = Node()
    w.f_val = 2
    bh.insert(w)
    print(bh.delete_min().f_val)
