from random import shuffle

# Set the initial state
# Tile A has value 1, B has value 2, C has value 3, agent has value 4 and the rest blank tiles have value 0
initial_state = [1, 0, 0, 0, 4, 0, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0]
# Set the goal state
goal = [0, 0, 0, 0, 4, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0]

# Create a class for initializing a node
# The state of  the node, its parent, the movement which has been made, the cost of the movement and the depth of the node are included
class Node:
    def __init__(self, state, parent, action, cost, depth):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth

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

# Expand node with random order(for deapth first search
def expand_node_for_dfs(node):
    expanded_nodes = []
    expanded_nodes.append(Node(movement(node.state, "up"), node, "up", node.cost + 1, node.depth + 1))
    expanded_nodes.append(Node(movement(node.state, "down"), node, "down", node.cost + 1, node.depth + 1))
    expanded_nodes.append(Node(movement(node.state, "left"), node, "left", node.cost + 1, node.depth + 1))
    expanded_nodes.append(Node(movement(node.state, "right"), node, "right", node.cost + 1, node.depth + 1))
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    # shuffle the children of the node
    shuffle(expanded_nodes)
    return expanded_nodes

def dfs(start, goal):
    # same logic with breadth first search, but in this case instead of a queue, there is a stack
    # in this case, the last node of the stack must be expanded
    stack_dfs = []
    stack_dfs.append(Node(start, None, None, 0, 0))
    explored = []
    flag = 0
    while flag != -1:
        if len(stack_dfs) == 0:
            flag = -1
            return None, len(explored)
        node = stack_dfs.pop(0)
        print("node state")
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
        explored.append(node.state)
        children = expand_node_for_dfs(node)
        i = 0
        for child in children:
            if child.depth == 4:
                flag = -1
            # if (child.state not in explored or child.state not in stack_dfs):   FOR GRAPH SEARCH
            # if find_state(child.state, goal) == 1:   WHEN THE PLACE OF THE AGENT IS IRRELEVANT
            stack_dfs.insert(i, child)
            i += 1
            if child.depth < 4:
                print("DFS with depth: " + str(child.depth))
                display_board(child.state)

result, amount = dfs(initial_state, goal)
