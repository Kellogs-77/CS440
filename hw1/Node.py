# Node class, for all your Node needs
# TODO change the values of the f, g, and h depending on how it should be

class Node:
    def __init__(self):
        self.position = ()
        self.parents = ()
        self.f_val = 0
        self.g_val = 0
        self.h_val = 0
        self.marked = False
    #SPRUHA: Added __repr__ method to support clean printing of nodes
    def __repr__(self):
        return "Pos:% s f:% s g:% s h:% s" % (self.position,self.f_val,self.g_val,self.h_val) 