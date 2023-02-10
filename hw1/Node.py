# Node class, for all your Node needs
# TODO change the values of the f, g, and h depending on how it should be

class Node:
    def __init__(self):
        self.parent = [None, None]
        self.f_val = 0
        self.g_val = 0
        self.h_val = 0
        self.marked = False
