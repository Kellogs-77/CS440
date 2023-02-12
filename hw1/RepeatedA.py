from Node import Node
from BinaryHeap import BinaryHeap
from MazeGenerator import MazeGenerator

closed_list = dict()
open_list = BinaryHeap()

def heuristic(end_position, start_positon):
    return (abs(end_position[0] - start_positon[0]) + abs(end_position[1]-start_positon[1]))

def check_blocked(cell):
    if(maze[cell[0], cell[1]] == 1):
        return True
    return False

def create_node(position, parent, g_val, h_val):
    n = Node()
    n.position = position
    n.parents.insert(1, parent)
    n.g_val = g_val
    n.h_val = h_val
    n.f_val = n.g_val + n.h_val
    return n

def RepeatedA(maze, start_state, target):
    #start the agent at the start state
    neighbors = [(0,1), (1,0), (0,-1), (-1,0)]
    agent_pos = start_state

    #set up the starting node
    start = create_node(tuple(agent_pos), [], 0, heuristic(target, start_state))
    
    #figure out if neighbors are blocked, if so, add them to the closed list
    #if neighbors are open, put them in the open list
    for i,j in neighbors:
        if (agent_pos[0] + i >= 0) and (agent_pos[1] + j >= 0):
            if check_blocked((i,j)):
                closed_list[(i, j)] = 0
            else:
                n = create_node((i,j), start.position, 1, heuristic(target, (i,j)))
                open_list.insert(n)
    
    closed_list[start.position] = 0
    counter = 1
    #set up the loop to continue until there is nothing in the open list  
    while(len(open_list.heap_list) > 1):



        current = open_list.delete_min()
        #if the current position is the target, return the path
        if current.position == tuple(target):
            return current.parents

        #get the neighbors of the current node otherwise
        

        closed_list[current.position] = 0
        print(closed_list)

    
    
    if agent_pos != target:
        print("Cannot reach target")
    



if __name__ == "__main__":
    #create the initial maze
    maze = MazeGenerator.create_maze(10,10)
    print(maze)
    RepeatedA(maze, [0,0], [len(maze)-1, len(maze[0])-1])