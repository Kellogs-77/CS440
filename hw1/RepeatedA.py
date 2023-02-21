from Node import Node
from BinaryHeap import BinaryHeap
from MazeGenerator import MazeGenerator
import sys
import numpy



closed_list = dict()
open_list = BinaryHeap()
path_list = dict()  # stores neighbors that I can pick from to travel to
temporary_tree = []
final_path = []
output_path = []
maze = []
empty_maze = []
target = ()
all_mazes = []
changed_heuristics = dict()
nodes_expanded = 0
for_nodes_expanded = []
back_nodes_expanded = []

def heuristic(end_position, start_positon):
    return (abs(end_position[0] - start_positon[0]) + abs(end_position[1]-start_positon[1]))


def check_blocked(cell):
    if (maze[cell[0], cell[1]] == 1):
        return True
    return False


def create_node(position, parent, g_val, h_val):
    n = Node()
    n.position = position
    n.parents = parent
    n.g_val = g_val
    n.h_val = h_val
    return n


def find_optimal_movement():
    min_val = min(path_list.values())

    for position in path_list:
        if path_list[position] == min_val:
            return position

    return -1


def check_in_bounds(tuple_to_check):
    return ((tuple_to_check[0] >= 0) and (tuple_to_check[1] >= 0)) and (tuple_to_check[0] < len(maze)) and (tuple_to_check[1] < len(maze))


def possible_movement():
    val = (len(open_list.heap_list) > 0)
    return val


def compounded_delete(position_check):
    min = open_list.delete_min()
    while (min.position != position_check):
        open_list.insert(min)
        min = open_list.delete_min()

# given a position, returns a list of neighbors


def get_neighbors(position):
    list_of_neighbors = []
    movements = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    for i, j in movements:
        possible_neighbor = (position[0] + i, position[1] + j)
        if check_in_bounds(possible_neighbor):
            list_of_neighbors.append(possible_neighbor)

    return list_of_neighbors

# initializes nodes with all the positions and h values for the maze

def initialize_maze_nodes(ch=0):
    maze_nodes = [[0]*len(maze) for i in range(len(maze))]
    if (ch == 0):
        # if called with no parameter, initalize maze normally
        for i in range(0, len(maze)):

            for j in range(0, len(maze)):

                n = create_node((i, j), (), 1000*100,
                                heuristic(target, (i, j)))
                maze_nodes[i][j] = n
    else:
        # if called with a parameter, initalize maze with updated
        # herusitic values where necessary
        for i in range(0, len(maze)):

            for j in range(0, len(maze)):

                if ((i, j) in changed_heuristics):
                    n = create_node((i, j), (), 1000*100,
                                    changed_heuristics[(i, j)])
                else:
                    n = create_node((i, j), (), 1000*100,
                                    heuristic(target, (i, j)))
                maze_nodes[i][j] = n
    return maze_nodes

# return maze with updated herusitic values
def change_heuristics():
    maze_nodes = initialize_maze_nodes(1)
    return maze_nodes


def traceback_path(maze_nodes, forward_or_back, start_position):
    final_path = []
    position = target

    if forward_or_back == 1:
        while (position != start_position):
            final_path.append(position)
            # set the position to the position of the nodes parent
            position = maze_nodes[position[0]][position[1]].parents

        final_path.append(start_position)

        return reversed(final_path)

    elif forward_or_back == -1:
        position = start_position
        while (position != target):
            final_path.append(position)
            # set the position to the position of the nodes parent
            position = maze_nodes[position[0]][position[1]].parents

        final_path.append(target)

        return final_path


def agent_traversal(path, record_maze):

    for i, j in path:

        if maze[i][j] == 1:
            record_maze[i][j] = 1

            return record_maze

        else:
            output_path.append((i, j))

    return record_maze


# given a start state and an end state, returns the shortest unblocked path from start to finish
def a_evaluator(current_node_position, maze_nodes, record_maze):
    # expand the node --> get a list of all the neighbors
    list_of_neighbors = get_neighbors(current_node_position)
    # add unblocked neighbors to the open list
    # add blocked neighbors to the closed list
    for i, j in list_of_neighbors:
        if record_maze[i][j] == 1:
            closed_list[(i, j)] = 0
        elif (record_maze[i][j] == 0) and ((i, j) not in closed_list):
            open_list.update_node((i, j), current_node_position, maze_nodes)
    # add the current node to the closed list
    closed_list[current_node_position] = 0
    return


def forward_a(start_pos, record_maze):
    maze_nodes = initialize_maze_nodes()
    start_node = maze_nodes[start_pos[0]][start_pos[1]]
    start_node.parents = ()
    start_node.g_val = 0
    start_node.h_val = heuristic(target, start_pos)
    start_node.f_val = start_node.g_val + start_node.h_val
    maze_nodes[start_pos[0]][start_pos[1]] = start_node
    open_list.insert(start_node)
    agent_pos = start_node.position
    while (agent_pos != target) and (len(open_list.heap_list) > 1):
        min = open_list.delete_min()
        agent_pos = min.position
        a_evaluator(agent_pos, maze_nodes, record_maze)

    if agent_pos == target:
        return traceback_path(maze_nodes, 1, start_node.position)
    elif len(open_list.heap_list) == 1:
        print("There is no escape")
        return []
    
def backward_a(start_pos, record_maze):
    maze_nodes = initialize_maze_nodes()

    start_node = maze_nodes[0][0]
    target_node = maze_nodes[target[0]][target[1]]
    target_node.g_val = 0
    target_node.h_val = heuristic(start_node.position, target)
    target_node.f_val = target_node.g_val + target_node.h_val
    maze_nodes[target[0]][target[1]] = target_node
    open_list.insert(target_node)
    agent_pos = target_node.position
    while (agent_pos != start_node.position) and (len(open_list.heap_list) > 1):
        min = open_list.delete_min()
        agent_pos = min.position
        a_evaluator(agent_pos, maze_nodes, record_maze)

    if agent_pos == start_node.position:
        return traceback_path(maze_nodes, -1, start_node.position)
        
    if len(open_list.heap_list) == 1:
        print("There is no escape")
        return []

# given a start state and an end state, returns the shortest unblocked path from start to finish

def adaptive_a_evaluator(current_node_position, start_pos, maze_nodes, record_maze):
    # update expanded node's heuristic
    s_goal = heuristic(target, start_pos)
    s = heuristic(current_node_position, start_pos)
    changed_heuristics[current_node_position] = (s_goal - s)

    # expand the node --> get a list of all the neighbors
    list_of_neighbors = get_neighbors(current_node_position)
    # add unblocked neighbors to the open list
    # add blocked neighbors to the closed list
    for i, j in list_of_neighbors:
        if record_maze[i][j] == 1:
            closed_list[(i, j)] = 0
        elif (record_maze[i][j] == 0) and ((i, j) not in closed_list):
            open_list.update_node((i, j), current_node_position, maze_nodes)
    # add the current node to the closed list
    closed_list[current_node_position] = 0
    return


def adaptive_a(start_pos, record_maze):
    maze_nodes = change_heuristics()

    start_node = maze_nodes[start_pos[0]][start_pos[1]]
    start_node.parents = ()
    start_node.g_val = 0
    start_node.h_val = heuristic(target, start_pos)
    start_node.f_val = start_node.g_val + start_node.h_val
    maze_nodes[start_pos[0]][start_pos[1]] = start_node
    open_list.insert(start_node)
    agent_pos = start_node.position
    while (agent_pos != target) and (len(open_list.heap_list) > 1):
        min = open_list.delete_min()
        agent_pos = min.position
        adaptive_a_evaluator(agent_pos, start_pos, maze_nodes, record_maze)

    if agent_pos == target:
        return traceback_path(maze_nodes, 1, start_node.position)
    elif len(open_list.heap_list) == 1:
        print("There is no escape")
        return []


def a_star_pathfinder(empty_maze, for_or_back):
    current_position = (0, 0)
    global for_nodes_expanded
    global back_nodes_expanded
    global nodes_expanded
    while current_position != target:

        neighbors = get_neighbors(current_position)

        for s, r in neighbors:
            empty_maze[s][r] = maze[s][r]

        if(for_or_back == 1):
            path = forward_a(current_position, empty_maze)
        else:
            path = backward_a(current_position, empty_maze)

        #path = backward_a(current_position, empty_maze)

        if not bool(path):
            return False
        else:
            empty_maze = agent_traversal(path, empty_maze)
            current_position = output_path[len(output_path) - 1]
            if for_or_back == 1:
                nodes_expanded += len(closed_list)
            else:
                nodes_expanded += len(closed_list)
            closed_list.clear()
            open_list.clear_heap()

def adaptive_star_pathfinder(empty_maze):
    current_position = (0, 0)
    changed_heuristics = dict()

    while current_position != target:

        neighbors = get_neighbors(current_position)

        for s, r in neighbors:
            empty_maze[s][r] = maze[s][r]

        path = adaptive_a(current_position, empty_maze)

        if not bool(path):
            return False
        else:
            empty_maze = agent_traversal(path, empty_maze)
            current_position = output_path[len(output_path) - 1]
            closed_list.clear()
            open_list.clear_heap()


if __name__ == "__main__":
    mazes = []
    for i in range(0,50):
        maze, empty_maze = MazeGenerator.create_maze(101, 101)
        mazes.append(maze)

    file = open("sample.txt", "w+")

    # Saving the array in a text file
    numpy.set_printoptions(threshold=sys.maxsize)
    content = str(mazes)
    file.write(content)
    file.close()
    
    numpy.set_printoptions(threshold=10)
    for i in range(0, 50):
         maze, empty_maze = MazeGenerator.create_maze(101, 101)
         maze = mazes[i]
         target = (len(maze) - 1, len(maze) - 1)
         print(maze)
         print("FORWARD A STAR     MAZE NUMBER {j}".format(j=i+1))
         if not a_star_pathfinder(empty_maze, 1):
            print(output_path)
            output_path.clear()
            closed_list.clear()
            open_list.clear_heap()
         for_nodes_expanded.append(nodes_expanded)
         nodes_expanded = 0

    for i in range(0, 50):
         maze, empty_maze = MazeGenerator.create_maze(101, 101)
         maze = mazes[i]
         target = (len(maze) - 1, len(maze) - 1)
         print(maze)
         print("BACKWARDS A STAR      MAZE NUMBER {j}".format(j=i+1))
         if not a_star_pathfinder(empty_maze, -1):
            print(output_path)
            output_path.clear()
            closed_list.clear()
            open_list.clear_heap()
            back_nodes_expanded.append(nodes_expanded)
            nodes_expanded = 0
    
    for i in range(0, 50):
        maze, empty_maze = MazeGenerator.create_maze(101, 101)
        maze = maze[i]
        target = (len(maze) - 1, len(maze) - 1)
        print(maze)
        print("ADAPTIVE A STAR       MAZE NUMBER {j}".format(j=i+1))
        if not adaptive_star_pathfinder(empty_maze):
            print(output_path)
        output_path.clear()
        closed_list.clear()
        open_list.clear_heap()

