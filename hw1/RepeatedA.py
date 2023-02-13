from Node import Node
from BinaryHeap import BinaryHeap
from MazeGenerator import MazeGenerator

closed_list = dict()
open_list = BinaryHeap()
path_list = dict() #stores neighbors that I can pick from to travel to
temporary_tree = []
final_path = []

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

def find_optimal_movement():
    min_val = min(path_list.values())

    for position in path_list:
        if path_list[position] == min_val:
            return position
    
    return -1

def check_in_bounds(tuple, target):
    return (tuple[0] >= 0 and tuple[1] >= 0 and tuple[0] <= target[0] and tuple[1] <= target[1])

def possible_movement():
    val = (len(open_list.heap_list) > 0)
    return val

def compounded_delete(position_check):
    min = open_list.delete_min()
    while (min.position != position_check):
        open_list.insert(min)
        min = open_list.delete_min()
    
#given a start state and an end state, returns the shortest unblocked path from start to finish 
def repeated_a(maze, start_state, target):
    #start the agent at the start state
    neighbors = [(0,1), (1,0), (0,-1), (-1,0)]
    agent_pos = start_state

    g = 1
    #figure out if neighbors are blocked; if so, add them to the closed list
    for i,j in neighbors:
        neighbor_pos = (agent_pos[0] + i, agent_pos[1] + j)
        if check_in_bounds(neighbor_pos, target):
            if (check_blocked(neighbor_pos) or (neighbor_pos in closed_list)):
                closed_list[neighbor_pos] = 0
            else:
                open_list.insert(create_node(neighbor_pos, agent_pos, g, heuristic(target, neighbor_pos)))
    
    compounded_delete(agent_pos)
    closed_list[agent_pos] = 0

    if not possible_movement():
        return False
 
    
    g = 2
    #iterate through the maze and find a path from start to target 
    while(agent_pos != tuple(target)):
        #add neighbors to a path list if you can move there
        for i,j in neighbors:
            if (agent_pos[0] + i >= 0 and agent_pos[0] + i < len(maze)) and (agent_pos[1] + j >= 0 and agent_pos[1] + j < len(maze)):
                position = agent_pos[0]+i, agent_pos[1]+j
                if position not in closed_list:
                    path_list[position] = heuristic(target, position) + g

        #check which neighbor has the smallest f value
       
        agent_pos = find_optimal_movement()
        temporary_tree.append(agent_pos)
        path_list.clear()
        g += 1
    
    return True
    
        

def forward_a_star(maze):
    #set up the starting node
    agent_position = (0,0)
    final_path.append(agent_position)
    target = (len(maze) - 1, len(maze) - 1)
    open_list.insert(create_node(agent_position, [], 0, heuristic(target, agent_position)))
    while(agent_position != target):
        if repeated_a(maze, agent_position, target):

            for pos in temporary_tree:
                #if the path is clear, add that to the tree
                if maze[pos[0]][pos[1]] == 0:
                    final_path.append(pos)
                else:
                    agent_position = final_path[len(final_path)-1]
                    break
            
            temporary_tree.clear()
        else: 
            print("There is no escape")
            break
    #agent movement until it finds a block
    



if __name__ == "__main__":
    #create the initial maze
    maze = MazeGenerator.create_maze(5,5)
    print(maze)
    forward_a_star(maze)
    print(final_path)