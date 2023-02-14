# Binary Heap class for all your Binary needs?
from Node import Node

#SPRUHA: Todo: Need to consider g_val as well
#SPRUHA: Todo: Need to locate a Node given position by iterating through the heap_list's Node objects. Need to start with index 1 as index 0 has just the integer 0
class BinaryHeap:
    def __init__(self):

        self.heap_list = [0]
        self.current_size = 1

    def sift_up(self, i):

        # While the element is not the root or the left element
        Stop = False
        while (i // 2 > 0) and Stop == False:
            #SPRUHA: handle top level nodes
            if (i==1 and self.current_size>2) or i==2:
                if self.heap_list[2].f_val < self.heap_list[1].f_val:
                    self.heap_list[2],self.heap_list[1]=self.heap_list[1],self.heap_list[2]
                elif self.heap_list[2].f_val == self.heap_list[1].f_val:
                    if self.heap_list[2].g_val > self.heap_list[1].g_val:
                        self.heap_list[2], self.heap_list[1] = self.heap_list[1], self.heap_list[2]
                return
            
            # If the element is less than its parent swap the elements
            #SPRUHA: Updated to swap the elements and not their f_val
            if self.heap_list[i].f_val < self.heap_list[i // 2].f_val:
                self.heap_list[i], self.heap_list[i //
                                                        2] = self.heap_list[i // 2], self.heap_list[i]
            elif self.heap_list[i].f_val == self.heap_list[i // 2].f_val:
                if self.heap_list[i].g_val > self.heap_list[i // 2].g_val:
                    self.heap_list[i], self.heap_list[i // 2] = self.heap_list[i // 2], self.heap_list[i]
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
        #SPRUHA: changed the second argument to be current_size-1 as it is being used as an index in sift_up
        self.sift_up(self.current_size-1)

    def sift_down(self, i):
        # if the current node has at least one child
        #SPRUHA: Changed the RHS of the comparison to be current_size-1 as RHS is an index while current size would be last index +1
        while (i * 2) <= self.current_size-1:
            #if heap_list has 1 or 2 items, then skip
            
            # Get the index of the min child of the current node
            mc = self.min_child(i)
            # Swap the values of the current element is greater than its min child
            #SPRUHA: Updated to swap the elements and not their f_val
            if self.heap_list[i].f_val > self.heap_list[mc].f_val:
                self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
            if self.heap_list[i].f_val == self.heap_list[mc].f_val:
                if self.heap_list[i].g_val < self.heap_list[mc].g_val:
                    self.heap_list[i], self.heap_list[mc] = self.heap_list[mc], self.heap_list[i]
                
            i = mc

    def min_child(self, i):
        # If the current node has only one child, return the index of the unique child
        #SPRUHA: Changed the RHS of the comparison to be current_size-1 as RHS is an index while current size would be last index +1
        if (i * 2)+1 > self.current_size-1:
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
        #SPRUHA: Maybe we should return a None instead of the string "Empty heap"?
        if len(self.heap_list) == 1:
            return 'Empty heap'

        # Get root of the heap (The min value of the heap)
        root = self.heap_list[1]
        
        #if there is only one Node, then just 
        # Move the last value of the heap to the root
        # SPRUHA:Added a check to skip swapping the last item for the root if we have only 2 elements - the dummy element of int 0 and the root
        if len(self.heap_list)>2:
            self.heap_list[1] = self.heap_list[self.current_size-1]

        # Pop the last value since a copy was set on the root
        *self.heap_list, _ = self.heap_list

        # Decrease the size of the heap
        self.current_size -= 1

        # Move down the root (value at index 1) to keep the heap property
        #Spruha: Added a check to sift_down only if we have more than 1 Node
        if self.current_size>2:
            self.sift_down(1)

        # Return the min value of the heap
        return root

    def update_node(self, node_position, parent_position, maze_nodes):       
        #iterate through the heap and find the child and prospective parent node
        counter = 0
        child = Node()
        parent = Node()
        i = 1
        child_position = 0
        child_found = False

        while counter < 2 and i < len(self.heap_list):

            node = self.heap_list[i]

            if node.position == node_position:
                child = node
                counter +=1
                child_position = i
                child_found = True
            if node.position == parent_position:
                parent = node
                counter += 1
            
            i += 1
        parent = maze_nodes[parent_position[0]][parent_position[1]] 
        #if child is false -> child does not exist, so need to update a child node in map and copy it into the heap
        if child_found == False:
            c_node = maze_nodes[node_position[0]][node_position[1]] 
            c_node.parents = parent_position
            p_node = maze_nodes[parent_position[0]][parent_position[1]]
            c_node.g_val = p_node.g_val + 1
            c_node.f_val = c_node.g_val + c_node.h_val
            self.insert(c_node)
            maze_nodes[node_position[0]][node_position[1]] = c_node
            return
        
        elif parent.position == child.parents:
            return
        #check if the prospective parent's g value + 1 is less than the g value of the node
        elif (parent.g_val + 1) < child.g_val:
            child.parents = parent.position
            child.g_val = parent.g_val + 1
            child.f_val = child.g_val + child.h_val
            maze_nodes[node_position[0]][node_position[1]] = child
            self.heap_list[child_position] = child 
            self.sift_up(child_position)
            return
        #if yes, replace the node's parent as the prospective parent, replace the g value, and recalculate the f value

    def clear_heap(self):
        while(len(self.heap_list) > 1):
            self.delete_min()
        

if __name__ == "__main__":	
    import PrintBinaryTree as pbt
    #SPRUHA - importing utility class to print binary trees	
    bh = BinaryHeap()
    
    #parent node
    actual_parent = Node()
    actual_parent.position = (0,0)
    actual_parent.parents = (0,0)
    actual_parent.f_val = 6
    actual_parent.g_val = 0
    actual_parent.h_val = 6
    child_1 = Node()
    child_1.position = (0,1)
    child_1.parents = (0,0)
    child_1.f_val = 6
    child_1.g_val = 1
    child_1.h_val = 5
    prospective_parent = Node()
    prospective_parent.position = (1,1)
    prospective_parent.parents = (1,0)
    prospective_parent.f_val = 6
    prospective_parent.g_val = 2
    prospective_parent.h_val = 4
    bh.insert(actual_parent)
    bh.insert(prospective_parent)
    bh.insert(child_1)
    bh.delete_min()
    
    print(bh)
    
