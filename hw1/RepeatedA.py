from Node import Node
from BinaryHeap import BinaryHeap
from MazeGenerator import MazeGenerator

closed_list = dict()
open_list = BinaryHeap()

def heuristic(end_position, start_positon):
    return (abs(end_position[0] - start_positon[0]) + abs(end_position[1]-start_positon[1]))

def RepeatedA(maze, start_state, target):
    #start the agent at the start state
    neighbors = [(0,1), (1,0), (0,-1), (-1,0)]
    agent_pos = start_state

    #set up the starting node
    start = Node()
    start.position = tuple(agent_pos)
    start.g_val = 0
    start.h_val = heuristic(target, agent_pos)
    start.f_val = start.g_val + start.h_val
    #figure out if neighbors are blocked, if so, add them to the closed list
    for i,j in neighbors:
        if (agent_pos[0] + i >= 0) and (agent_pos[1] + j >= 0):
            if maze[i][j] == 1:
                closed_list[(i, j)] = 0
            else:
                n = Node()
                n.position = (i,j)
                n.parents.insert(1, start.position)
                n.g_val = 1
                n.h_val = heuristic(target, n.position)
                n.f_val = n.g_val + n.h_val
                open_list.insert(n)

    while(len(open_list.heap_list) > 1):
        min = open_list.delete_min()

        closed_list[tuple(agent_pos)] = 0


    #set up the loop
    
    if agent_pos != target:
        print("Cannot reach target")
    



if __name__ == "__main__":
    #create the initial maze
    maze = MazeGenerator.create_maze(10,10)
    print(maze)
    RepeatedA(maze, [0,0], [len(maze)-1, len(maze[0])-1])