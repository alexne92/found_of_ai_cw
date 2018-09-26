import random
from random import shuffle
import math
import matplotlib.pyplot as plt
import numpy as np
initial_state = [0,0,0, 0,0,0, 1,2,4]
#initial_state = [0,1,0, 0,4,0, 0,2,0,]
#initial_state = [0,1,0, 4,0,0, 0,2,0]
#initial_state = [0,0,0, 0,1,2, 0,0,4]
goal_state0 = [0,0,0, 0,1,0, 0,2,4]
goal_state1 = [0,4,0, 0,1,0, 0,2,0]
goal_state2 = [0,0,0, 0,1,0, 4,2,0]
goal_state3 = [0,0,0, 0,1,4, 0,2,0]
goal_state4 = [0,0,0, 4,1,0, 0,2,0]
goal_state5 = [0,0,4, 0,1,0, 0,2,0]
goal_state6 = [4,0,0, 0,1,0, 0,2,0]
goal_state = [goal_state0, goal_state1, goal_state2, goal_state3, goal_state4, goal_state5, goal_state6]

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

def up(state):
    new_state = list(state)
    index = new_state.index(4)
    if index not in range(3):
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None
def down(state):
    new_state = list(state)
    index = new_state.index(4)
    if index not in range(6,9):
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None
def left(state):
    new_state = list(state)
    index = new_state.index(4)
    if index not in range(0,9,3):
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None
def right(state):
    new_state = list(state)
    index = new_state.index(4)
    if index not in range(2,9,3):
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        return None

def display_board( state ):
    if state == None:
        pass
    else:
        new_state_disp = state[:]
        index_a = new_state_disp.index(1)
        index_b = new_state_disp.index(2)
        #index_c = new_state_disp.index(3)
        index_agent = new_state_disp.index(4)
        new_state_disp[index_a] = 'A'
        new_state_disp[index_b] = 'B'
        #new_state_disp[index_c] = 'C'
        new_state_disp[index_agent] = 'X'
        new_state_disp = [ x if x!= 0 else " " for x in new_state_disp ]
        print("-------------")
        print("| %s | %s | %s |" % (new_state_disp[0], new_state_disp[1], new_state_disp[2]) )
        print("-------------")
        print("| %s | %s | %s |" % (new_state_disp[3], new_state_disp[4], new_state_disp[5] ) )
        print("-------------")
        print("| %s | %s | %s |" % (new_state_disp[6], new_state_disp[7], new_state_disp[8]) )
        print("-------------")

def create_node(state, parent, action, cost, depth):
    return Node(state, parent, action, cost, depth)

def expand_node( node ):
    #Returns a list of expanded nodes
    expanded_nodes = []
    #number = random.randint(1,4)
    expanded_nodes.append( create_node( up( node.state ), node, "up", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( down( node.state ), node, "down", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( left( node.state ), node, "left", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( right( node.state),  node, "right", node.cost + 1, node.depth + 1 ) )
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
    return expanded_nodes

def expand_node_for_dfs( node ):
    #Returns a list of expanded nodes
    expanded_nodes = []
    #number = random.randint(1,4)
    expanded_nodes.append( create_node( up( node.state ), node, "up", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( down( node.state ), node, "down", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( left( node.state ), node, "left", node.cost + 1, node.depth + 1 ) )
    expanded_nodes.append( create_node( right( node.state),  node, "right", node.cost + 1, node.depth + 1 ) )
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
    shuffle(expanded_nodes)
    return expanded_nodes

def create_node_for_a_star(state, parent, action, cost, depth, h_cost):
    return A_star_node(state, parent, action, cost, depth, h_cost)

def expand_node_for_a_star( node,goal ):
    #Returns a list of expanded nodes
    expanded_nodes = []
    #number = random.randint(1,4)
    expanded_nodes.append( create_node_for_a_star( up( node.state ), node, "up", node.cost + 1, node.depth + 1, h(up( node.state ), goal) ) )
    expanded_nodes.append( create_node_for_a_star( down( node.state ), node, "down", node.cost + 1, node.depth + 1, h(down( node.state ), goal) ) )
    expanded_nodes.append( create_node_for_a_star( left( node.state ), node, "left", node.cost + 1, node.depth + 1, h(left( node.state ), goal) ) )
    expanded_nodes.append( create_node_for_a_star( right( node.state),  node, "right", node.cost + 1, node.depth + 1, h(right( node.state ), goal) ) )
    # Filter the list and remove the nodes that are impossible (move function returned None)
    expanded_nodes = [node for node in expanded_nodes if node.state != None] #list comprehension!
    return expanded_nodes

def find_state(a,b):
    target = 0
    for i in b:
        if a == i:
            target += 1
    return target

def bfs( start, goal ):
   #Performs a breadth first search from the start state to the goal
    # A list (can act as a queue) for the nodes.
    list_bfs = []
    # Create the queue with the root node in it.
    list_bfs.append( create_node( start, None, None, 0, 0 ) )
    explored = []
    counter = 1
    i = 0
    flag = 0
    while flag !=-1 :
    #while True:
        # We've run out of states, no solution.
        if len( list_bfs ) == 0:
            flag = -1
            return None, len(explored)
        # take the node from the front of the queue
        node = list_bfs.pop(0)
       # check if this node is the goal
        if node.state == goal:
           # if it is, initialise a list which will contain the actions of the agent
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
        # create the children of the node
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

def find_index(node):
    tile_A = node.index(1)
    tile_B = node.index(2)
    tile_agent = node.index(4)
    row_A = find_row( tile_A )
    column_A = find_column( tile_A )
    row_B = find_row( tile_B )
    column_B = find_column( tile_B )
    row_agent = find_row(tile_agent)
    column_agent = find_column(tile_agent)
    return list([row_A, column_A, row_B, column_B, row_agent, column_agent])

def find_row(r):
    row = 0
    if r in range(3):
        row = 0
    elif r in range(3,6):
        row = 1
    elif r in range(6,9):
        row = 2
    return row

def find_column(c):
    column = 0
    if c in range(0,9,3):
        column = 0
    elif c in range(1,9,3):
        column = 1
    elif c in range(2,9,3):
        column = 2
    return column


def h( state, goal ):
    if state == None:
        return None
    else:
        score = 0
        list_of_state = find_index( state )
        list_of_goal = find_index( goal )
        for i in range(len(list_of_state)):
            score += abs( list_of_state[i] - list_of_goal[i] )
        return score

def visual_result(move,state):
    new_state = list(state)
    new_position = list(new_state)
    if move == "up":
        new_position = up(new_state)
    elif move == "down":
        new_position = down(new_state)
    elif move == "left":
        new_position = left(new_state)
    elif move == "right":
        new_position = right(new_state)
    return new_position

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
        result, amount = ids(initial_state, goal, 10)
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

    print(nodes[i])
    print(len(result), " moves")
plt.bar(range(len(nodes)),nodes)
plt.xticks(range(len(nodes)), ('DFS', 'BFS', 'IDS', 'A*'))
plt.title('Nodes expanded for each method')
plt.savefig('bar3.png')
plt.show()
print(nodes)
