# Set the initial state
# Tile A has value 1, B has value 2, C has value 3, agent has value 4 and the rest blank tiles have value 0
initial_state = [1, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0]
# Set the goal state
goal = [0, 0, 0, 0, 4, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0]

# Special case for A * - same as class Node plus storing the result of the heuristic function
class A_star_node:
    def __init__(self, state, parent, action, cost, depth, h_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        self.h_cost = h_cost

# Function for movement
# When direction is up, the procedure is described in details. The rest directions have the same logic
def movement(state, direction):
    # copy  the state
    new_state = list(state)
    # find the index of the agent
    index = new_state.index(4)
    # if the agent goes up
    if direction == "up":
        if index not in range(4):
            # find the value of the tile where the agent is going to move
            temp = new_state[index - 4]
            # move the agent to the new location
            new_state[index - 4] = new_state[index]
            # set the value, that was temporaryy stored, to the tile that the agent was located
            new_state[index] = temp
            return new_state
    # if the agent goes down
    if direction == "down":
        if index not in range(12, 16):
            temp = new_state[index + 4]
            new_state[index + 4] = new_state[index]
            new_state[index] = temp
            return new_state
    # if the agent goes left
    if direction == "left":
        if index not in range(0, 16, 4):
            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp
            return new_state
    # if the agent goes right
    if direction == "right":
        if index not in range(3, 16, 4):
            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp
            return new_state
    # if the agent is unable to move due to his position on the grid, return None
    else:
        return None

# Visualise the grid world
def display_board(state):
    # if none state is given, pass the function
    if state == None:
        pass
    else:
        # copy the list
        new_state_disp = state[:]
        # find the location of the tiles A, B, C and agent
        index_a = new_state_disp.index(1)
        index_b = new_state_disp.index(2)
        index_c = new_state_disp.index(3)
        index_agent = new_state_disp.index(4)
        # replace the values with their visual form
        new_state_disp[index_a] = 'A'
        new_state_disp[index_b] = 'B'
        new_state_disp[index_c] = 'C'
        new_state_disp[index_agent] = 'X'
        new_state_disp = [x if x != 0 else " " for x in new_state_disp]
        # print the grid
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[0], new_state_disp[1], new_state_disp[2], new_state_disp[3]))
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[4], new_state_disp[5], new_state_disp[6], new_state_disp[7]))
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[8], new_state_disp[9], new_state_disp[10], new_state_disp[11]))
        print("-----------------")
        print(
            "| %s | %s | %s | %s |" % (new_state_disp[12], new_state_disp[13], new_state_disp[14], new_state_disp[15]))
        print("-----------------")

# Expand node while include the heuristic cost
def expand_node_for_a_star(node, goal):
    expanded_nodes = []
    expanded_nodes.append(A_star_node(movement(node.state, "up"), node, "up", node.cost + 1, node.depth + 1,
                                      h(movement(node.state, "up"), goal)))
    expanded_nodes.append(A_star_node(movement(node.state, "down"), node, "down", node.cost + 1, node.depth + 1,
                                      h(movement(node.state, "down"), goal)))
    expanded_nodes.append(A_star_node(movement(node.state, "left"), node, "left", node.cost + 1, node.depth + 1,
                                      h(movement(node.state, "left"), goal)))
    expanded_nodes.append(A_star_node(movement(node.state, "right"), node, "right", node.cost + 1, node.depth + 1,
                                      h(movement(node.state, "right"), goal)))
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    return expanded_nodes

def a_star(start, goal):
    # initialise the list of the nodes for expansion
    nodes = []
    # insert the initial state
    nodes.append(A_star_node(start, None, None, 0, 0, h(start, goal)))
    explored = []
    flag = 0
    while flag != -1:
        if len(nodes) == 0:
            return None, len(explored)
        # sort the nodes by the the function f(n) = g(n) + h(n)
        nodes.sort(key=lambda x: x.depth + x.h_cost)
        # take the node with the smallest value for the f(n)
        node = nodes.pop(0)
        print("A* with depth: " + str(node.depth))
        print(node.h_cost+node.depth)
        display_board(node.state)
        if node.state == goal:
            moves = []
            temp = node
            while True:
                moves.insert(0, temp.action)
                if temp.depth == 1:
                    break
                temp = temp.parent
            flag = -1
            return moves, len(explored)
        explored.append(node)
        children = expand_node_for_a_star(node, goal)
        for child in children:
            # if (child.state not in explored or child.state not in nodes):
            nodes.append(child)
            if child.depth == 4:
                flag = -1
                break

# find the place of each tile in the board
def find_index(node):
    # take the place of the tiles in the list
    tile_A = node.index(1)
    tile_B = node.index(2)
    tile_C = node.index(3)
    tile_agent = node.index(4)
    # set the row and the colum for each tile
    row_A = find_row(tile_A)
    column_A = find_column(tile_A)
    row_B = find_row(tile_B)
    column_B = find_column(tile_B)
    row_C = find_row(tile_C)
    column_C = find_column(tile_C)
    row_agent = find_row(tile_agent)
    column_agent = find_column(tile_agent)
    return list([row_A, column_A, row_B, column_B, row_C, column_C, row_agent, column_agent])

# Functions for finding the row and the column of a tile depending on their place in the list
def find_row(r):
    # initialise the number of the row
    row = 0
    # if the tile is in the first row
    if r in range(4):
        # set the row equal to 0
        row = 0
    # else if the tile is in the second row
    elif r in range(4, 8):
        # set the row equal to 1
        row = 1
    # else if the tile is in the third row
    elif r in range(8, 12):
        # set the row equal to 2
        row = 2
    # else if the tile is in the fourth row
    elif r in range(12, 16):
        # set the row equal to 3
        row = 3
    # return the number of the row
    return row

def find_column(c):
    # same logic with the find_row function
    column = 0
    if c in range(0, 16, 4):
        column = 0
    elif c in range(1, 16, 4):
        column = 1
    elif c in range(2, 16, 4):
        column = 2
    elif c in range(3, 16, 4):
        column = 3
    return column

# heuristic function which computed the estimated cost from the node to the goal, using the Manhatan distance
def h(state, goal):
    # if no state is given, return none
    if state == None:
        return None
    else:
        # initialise the cost
        score = 0
        # find the position of each tile for the current node and the goal state
        list_of_state = find_index(state)
        list_of_goal = find_index(goal)
        # compare each tile through the Manhatan distance
        for i in range(len(list_of_state)):
            score += abs(list_of_state[i] - list_of_goal[i])
        # return cost
        return score

result, amount = a_star(initial_state, goal)
