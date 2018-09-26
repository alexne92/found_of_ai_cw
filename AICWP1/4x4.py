from random import shuffle
import math
import matplotlib.pyplot as plt


#Set the initial state
#Tile A has value 1, B has value 2, C has value 3, agent has value 4 and the rest blank tiles have value 0
#initial_state = [0,0,0,0, 0,0,0,0, 0,0,0,0, 1,2,3,4]
initial_state = [1,0,0,0, 4,0,0,0, 0,2,0,0, 0,3,0,0]
#Set the goal state
goal_state0 = [0,0,0,0, 0,1,0,0, 0,2,0,0, 0,3,0,4]
goal_state1 = [0,0,0,0, 0,1,0,0, 0,2,0,0, 0,3,4,0]
goal_state2 = [0,0,0,0, 0,1,0,0, 0,2,0,0, 4,3,0,0]
goal_state3 = [0,0,0,0, 0,1,0,0, 0,2,0,4, 0,3,0,0]
goal_state4 = [0,0,0,0, 0,1,0,0, 0,2,4,0, 0,3,0,0]
goal_state5 = [0,0,0,0, 0,1,0,0, 4,2,0,0, 0,3,0,0]
goal_state6 = [0,0,0,0, 0,1,0,4, 0,2,0,0, 0,3,0,0]
goal_state7 = [0,0,0,0, 0,1,4,0, 0,2,0,0, 0,3,0,0]
goal_state8 = [0,0,0,0, 4,1,0,0, 0,2,0,0, 0,3,0,0]
goal_state9 = [0,0,0,4, 0,1,0,0, 0,2,0,0, 0,3,0,0]
goal_state10 = [0,0,4,0, 0,1,0,0, 0,2,0,0, 0,3,0,0]
goal_state11 = [0,4,0,0, 0,1,0,0, 0,2,0,0, 0,3,0,0]
goal_state12 = [4,0,0,0, 0,1,0,0, 0,2,0,0, 0,3,0,0]
goal_state = [goal_state0, goal_state1, goal_state2, goal_state3, goal_state4, goal_state5, goal_state6, goal_state7, goal_state8, goal_state9, goal_state10, goal_state11, goal_state12]

#Create a class for initializing a node
#The state of  the node, its parent, the movement which has been made, the cost of the movement and the depth of the node are included
class Node:
    def __init__( self, state, parent, action, cost, depth):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth

#Special case for A * - same as class Node plus storing the result of the heuristic function
class A_star_node:
    def __init__( self, state, parent, action, cost, depth, h_cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.depth = depth
        self.h_cost = h_cost

#Function for movement
#When direction is up, the procedure is described in details. The rest directions have the same logic
def movement(state, direction):
    # copy  the state
    new_state = list(state)
    # find the index of the agent
    index = new_state.index(4)
    #if the agent goes up
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
    #if the agent is unable to move due to his position on the grid, return None
    else:
        return None

#Visualise the grid world
def display_board( state ):
    #if none state is given, pass the function
    if state == None:
        pass
    else:
        #copy the list
        new_state_disp = state[:]
        #find the location of the tiles A, B, C and agent
        index_a = new_state_disp.index(1)
        index_b = new_state_disp.index(2)
        index_c = new_state_disp.index(3)
        index_agent = new_state_disp.index(4)
        #replace the values with their visual form
        new_state_disp[index_a] = 'A'
        new_state_disp[index_b] = 'B'
        new_state_disp[index_c] = 'C'
        new_state_disp[index_agent] = 'X'
        new_state_disp = [ x if x!= 0 else " " for x in new_state_disp ]
        #print the grid
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[0], new_state_disp[1], new_state_disp[2], new_state_disp[3]) )
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[4], new_state_disp[5], new_state_disp[6], new_state_disp[7]) )
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[8], new_state_disp[9], new_state_disp[10], new_state_disp[11]) )
        print("-----------------")
        print("| %s | %s | %s | %s |" % (new_state_disp[12], new_state_disp[13], new_state_disp[14], new_state_disp[15]) )
        print("-----------------")

#Visualise the sequence of movement for the agent in order to reach the solution
def visual_result(move,state):
    #copy the list of the state
    new_state = list(state)
    #initialise new position
    new_position = list(new_state)
    #set the new state, depending on the movement
    if move == "up":
        new_position = movement( new_state, "up" )
    elif move == "down":
        new_position = movement( new_state, "down" )
    elif move == "left":
        new_position = movement( new_state, "left" )
    elif move == "right":
        new_position = movement( new_state, "right" )
    #return the new state
    return new_position

#Expand node with the possible movements
def expand_node( node ):
    #initialise the list for expanded nodes
    expanded_nodes = []
    #for each movement, create a new node and store it to the list
    expanded_nodes.append( Node( movement( node.state, "up" ), node, "up", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "down" ), node, "down", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "left" ), node, "left", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "right" ),  node, "right", node.cost + 1, node.depth + 1 ) )
    #delete the nodes that there is no movement able to be made
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    return expanded_nodes

#Expand node with random order(for deapth first search
def expand_node_for_dfs( node ):
    expanded_nodes = []
    expanded_nodes.append( Node( movement( node.state, "up" ), node, "up", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "down" ), node, "down", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "left" ), node, "left", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( Node( movement( node.state, "right" ),  node, "right", node.cost + 1, node.depth + 1 ) )
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    #shuffle the children of the node
    shuffle(expanded_nodes)
    return expanded_nodes

#Expand node while include the heuristic cost
def expand_node_for_a_star( node,goal ):
    expanded_nodes = []
    expanded_nodes.append( A_star_node( movement( node.state, "up" ), node, "up", node.cost + 1, node.depth + 1, h(movement( node.state, "up" ), goal) ) )
    expanded_nodes.append( A_star_node( movement( node.state, "down" ), node, "down", node.cost + 1, node.depth + 1, h(movement( node.state, "down" ), goal) ) )
    expanded_nodes.append( A_star_node( movement( node.state, "left" ), node, "left", node.cost + 1, node.depth + 1, h(movement( node.state, "left" ), goal) ) )
    expanded_nodes.append( A_star_node( movement( node.state, "right" ),  node, "right", node.cost + 1, node.depth + 1, h(movement( node.state, "right" ), goal) ) )
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    return expanded_nodes

#Functions that compares a list with lists which are contained in a bigger list
#This functions is used for problems where the final place of the agent is not important(not applicable in A*)
def find_state(a,b):
    #function receives a list and a list of lists
    #initialise a constant as 0. If there is a match between two lists, the constant turns into 1
    target = 0
    #for each list of the big list
    for i in b:
        #if a match between the lists is found
        if a == i:
            #Change the value of the constant
            target += 1
    #return the result of comparison between the lists
    return target

def bfs( start, goal ):
    #initialise the list of the nodes for exploration/expansion
    list_bfs = []
    # Insert the initial state
    list_bfs.append( Node( start, None, None, 0, 0 ) )
    #initialise the list that stores which nodes were expanded
    explored = []
    counter = 0
    #set a constant which is used to break the loop if the solution is found
    flag = 0
    while flag != -1:
        #if there are no nodes left for expansion
        if len( list_bfs ) == 0:
            flag = -1
            return None, len(explored)
        #use the first node of the list (FIFO)
        node = list_bfs.pop(0)
        #check if this node is the goal
        if node.state == goal:
            #if it is, initialise a list which will contain the actions of the agent
            moves = []
            # temporary save the node in a variable
            temp = node
            # while there movements left
            while True:
                # insert each movement at the begining of the list
                moves.insert(0, temp.action)
                # if the state is one after the initial state
                if temp.depth == 1:
                    # stop the loop
                    break
                # swap place of the child with its parent
                temp = temp.parent
            # terminate the while loop
            flag = -1
            # return the moves that the agent did plus the nodes expanded
            return moves, len(explored)
        # store the expanded node to the relevant list
        explored.append(node.state)
        #create the children of the node
        children = expand_node(node)
        for child in children:
            list_bfs.append(child)

def dfs( start, goal ):
    #same logic with breadth first search, but in this case instead of a queue, there is a stack
    #in this case, the last node of the stack must be expanded
    stack_dfs = []
    stack_dfs.append( Node( start, None, None, 0, 0 ) )
    explored = []
    flag = 0
    while flag!= -1:
        if len( stack_dfs ) == 0:
            flag = -1
            return None, len(explored)
        # use the first node of the lstack (LIFO)
        node = stack_dfs.pop(0)
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
        #set the place for the first child
        i = 0
        for child in children:
            #if (child.state not in explored or child.state not in stack_dfs):   FOR GRAPH SEARCH
                #if find_state(child.state, goal) == 1:   WHEN THE PLACE OF THE AGENT IS IRRELEVANT
                stack_dfs.insert(i,child)
                i+=1 #set place for the rest children

def ids_limit( start, goal, depth ):
    #same as depth first search with the addition that a limit is inserted for the depth of the search
    depth_limit = depth
    stack_ids = []
    stack_ids.append( Node( start, None, None, 0, 0 ) )
    explored = []
    flag = 0
    while flag != -1:
        if len( stack_ids ) == 0:
            flag = -1
            return None, len(explored)
        node = stack_ids.pop(0)
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
        #as long as the limit of depth is not reached, continue with this path
        if node.depth < depth_limit:
            explored.append(node.state)
            children = expand_node(node)
            for child in children:
                #if (child.state not in explored or child.state not in stack_dfs):
                    #if find_state(child.state, goal) == 1:
                    stack_ids.insert(0,child)

def ids( start, goal, depth ):
    #store the amount of nodes expanded for each depth
    total_amount = 0
    #iterate the ids_limit function for each depth until it reaches the limit that the user gives
    for i in range( depth + 1 ): #adding one so as to implement the ids for the limit that user gives
        result, amount = ids_limit( start, goal, i )
        #add the nodes expanded for each iteration
        total_amount += amount
        #if the goal is reached, return the result and the computational time and stop the loop
        if result != None:
            return result, total_amount
            break
    #if the goal is not reached, return None as a result along with the amount of nodes expanded
    if result == None:
        return result, total_amount

def a_star(start, goal):
    #initialise the list of the nodes for expansion
    nodes = []
    #insert the initial state
    nodes.append( A_star_node( start, None, None, 0, 0, h( start, goal ) ) )
    explored = []
    flag = 0
    while flag!= -1:
        if len(nodes)== 0:
            return None, len(explored)
        #sort the nodes by the the function f(n) = g(n) + h(n)
        nodes.sort(key=lambda x: x.depth + x.h_cost)
        #take the node with the smallest value for the f(n)
        node = nodes.pop(0)
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
        children = expand_node_for_a_star(node,goal)
        for child in children:
            #if (child.state not in explored or child.state not in nodes):
                    nodes.append(child)

#find the place of each tile in the board
def find_index(node):
    #take the place of the tiles in the list
    tile_A = node.index(1)
    tile_B = node.index(2)
    tile_C = node.index(3)
    tile_agent = node.index(4)
    #set the row and the colum for each tile
    row_A = find_row( tile_A )
    column_A = find_column( tile_A )
    row_B = find_row( tile_B )
    column_B = find_column( tile_B )
    row_C = find_row(tile_C)
    column_C = find_column(tile_C)
    row_agent = find_row(tile_agent)
    column_agent = find_column(tile_agent)
    return list([row_A, column_A, row_B, column_B, row_C, column_C, row_agent, column_agent])

#Functions for finding the row and the column of a tile depending on their place in the list
def find_row(r):
    #initialise the number of the row
    row = 0
    #if the tile is in the first row
    if r in range(4):
        #set the row equal to 0
        row = 0
    #else if the tile is in the second row
    elif r in range(4,8):
        # set the row equal to 1
        row = 1
    # else if the tile is in the third row
    elif r in range(8,12):
    #set the row equal to 2
        row = 2
    # else if the tile is in the fourth row
    elif r in range(12, 16):
        # set the row equal to 3
        row = 3
    #return the number of the row
    return row

def find_column(c):
    #same logic with the find_row function
    column = 0
    if c in range(0,16,4):
        column = 0
    elif c in range(1,16,4):
        column = 1
    elif c in range(2,16,4):
        column = 2
    elif c in range(3,16,4):
        column = 3
    return column

#heuristic function which computed the estimated cost from the node to the goal, using the Manhatan distance
def h( state, goal ):
    #if no state is given, return none
    if state == None:
        return None
    else:
        #initialise the cost
        score = 0
        #find the position of each tile for the current node and the goal state
        list_of_state = find_index( state )
        list_of_goal = find_index( goal )
        #compare each tile through the Manhatan distance
        for i in range(len(list_of_state)):
            score += abs( list_of_state[i] - list_of_goal[i] )
        #return cost
        return score

#initialise a list that keeps the nodes which were expanded for each search method
nodes = []
#set the desired goal
goal = goal_state0
for i in range(4):
    if i==0:
        #implement the depth first search
        result, amount = dfs(initial_state, goal)
    elif i == 1:
        #implement the breadth first search
        result, amount = bfs(initial_state, goal)
    elif i == 2:
        #implement the iterative deeping search
        #here, the depth is 10(change this number for different depth)
        result, amount = ids(initial_state, goal, 500000)
    else:
        #implement the A* heuristic search
        result, amount = a_star(initial_state, goal)
    #store the amount of nodes for each method
    nodes.append(amount)
    if result == None:
        print("This search method didn't solve the problem")
    else:
        print(result)
        print(len(result), " moves")
        display_board(initial_state)
        for iter in range(len(result)):
            if iter == 0:
                a = visual_result(result[iter],initial_state)
                display_board(a)
            elif iter == 1:
                temp = a
                b = visual_result(result[iter], temp)
                c = b
                display_board(c)
            else:
                temp = c
                b = visual_result(result[iter], temp)
                c = b
                display_board(c)
        print(len(result), " moves")
    print(nodes[i])

plt.bar(range(len(nodes)),nodes, color = 'r')
plt.ylabel('Nodes expanded')
plt.xlabel('Search methods')
plt.xticks(range(len(nodes)), ('DFS', 'BFS', 'IDS', 'A*'))
plt.title('Nodes expanded for each search method')
plt.savefig('bar4.png')
plt.show()
print(nodes)
display_board(initial_state)
