#import random
def visualise_board(board):
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
    print('-----------')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('-----------')
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])

def Pick_letter():
    print('Type the letter of your choice for this game [X/O]: ')
    letter = input().upper()
    while letter not in ["X", "O"]:
        print("This letter is not available. Options are X or O. Please follow the instructions.")
        print('Type the letter of your choice for this game [X/O]: ')
        letter = input().upper()
    if letter == "X":
        return "X", "O"
    else:
        return "O", "X"

def Pick_turn():
    print("Do you want to play first? [y/n]")
    turn = input().upper()
    while turn not in ["Y", "N"]:
        print("This option is not available. Type y if you want to play first, otherwise type n.")
        print("Do you want to play first? [y/n]")
        turn = input().upper()
    if turn == "Y":
        return "player"
    elif turn == "N":
        return "computer"

def allowed_moves(board, letter):
    list_of_moves = []
    for i in range(9):
        new_board = board[:]
        if rule(new_board, i):
            list_of_moves.append(make_move(new_board,letter,i)) #list which containts the next possible moves, based on the board
    return list_of_moves

def find_score(board, computer_letter, player_letter):
    if winning_condition(board, player_letter): #if the machine wins
        return -100
    elif winning_condition(board, computer_letter): #if player wins
        return 100
    elif full_board(board): #if it is a tie
        return 0
    else: #if the game is still on
        return 1


def minimax(board, depth, computer_letter, player_letter, maxplayer, alpha, beta):
    score = find_score(board, computer_letter, player_letter)
    if score == 100 or score == -100 or score == 0 or depth == 0:
        return score, board
    if maxplayer:
        best = -100
        best_state = None
        states = allowed_moves(board, computer_letter)
        for state in states:
            v, move = minimax(state, depth - 1, computer_letter, player_letter, False, alpha, beta)
            if v > best:
                best_state = state
                best = v
            if best > alpha:
                alpha = best
            if alpha >= beta:
                break
        return best, best_state
    else:
        best = 100
        best_state = None
        states = allowed_moves(board, player_letter)
        for state in states:
            v, move = minimax(state, depth -1,  computer_letter, player_letter, True, alpha, beta)
            if v <= best:
                best_state = state
                best = v
            if best < alpha:
                alpha = best
            if alpha >= beta:
                break
        return best, best_state


def winning_condition(board,letter):
    if ((board[6] == letter and board[7] == letter and board[8] == letter) or # check the top line for win
    (board[3] == letter and board[4] == letter and board[5] == letter) or # across the middle
    (board[0] == letter and board[1] == letter and board[2] == letter) or # across the bottom
    (board[6] == letter and board[3] == letter and board[0] == letter) or # down the left side
    (board[7] == letter and board[4] == letter and board[1] == letter) or # down the middle
    (board[8] == letter and board[5] == letter and board[2] == letter) or # down the right side
    (board[6] == letter and board[4] == letter and board[2] == letter) or # diagonal
    (board[8] == letter and board[4] == letter and board[0] == letter)): # diagonal
        return  True

def rule(board, move):
    #if the move is eligible, return true
    if board[move] == " ":
        return True
    else:
        return False

def pick_move(board):
    move = " "
    while move not in range(9) or not rule(board, int(move)):
        print('What is your next move? (0-8)')
        move = int(input())
        if move not in range(9):
            print("This option is not available. Please choose a number from 0 to 8.")
        if not rule(board, int(move)):
            print("This option is not available, because someone has used this move.")
    return int(move)
"""
This function was used for random moves
def chooseRandomMoveFromList(board):
    possibleMoves = []
    for i in list(range(1,10)):
        if rule(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return random.choice(possibleMoves)
    else:
        return None
"""
def make_move(board, letter, move):
    new_board = list(board)
    new_board[move] = letter
    return new_board
"""
function for making the machine move randomly(not used)
def computer_move(board, computer_letter, player_letter ):
    for i in range(9):
        new_board = list(board)
        if rule(new_board, i):
            make_move(new_board, computer_letter, i)
            if winning_condition(new_board, computer_letter):
                return i
                pass

    for i in range(1, 10):
        new_board = list(board)
        if rule(new_board, i):
            make_move(new_board, player_letter, i)
            if winning_condition(new_board, player_letter):
                return i
                pass

    return chooseRandomMoveFromList(board)
"""
def full_board(board):
    # Return True if every space on the board has been taken. Otherwise return False.
    for i in range(9):
        if rule(board, i):
            return False
            pass
    return True

print('Welcome to Tic Tac Toe!')
board = [" "] * 9
player_letter, computer_letter = Pick_letter()
turn = Pick_turn()

print("This is the initial board:")
visualise_board(board)
print("And these are the numbers who correspond to the available moves:")
visualise_board(["0","1","2","3","4","5","6","7","8"])

game_is_on = True
while game_is_on:
    if turn == "player":
        move = pick_move(board)
        board = make_move(board, player_letter, move)
        visualise_board(board)
        if winning_condition(board, player_letter):
            print("Congratulations! You have won!")
            game_is_on = False
        else:
            if full_board(board):
                print("That's a tie. Well played!")
                game_is_on = False
                break
            else:
                turn = "computer"
    elif turn == "computer":
        print("This is what the computer chose to play:")
        score, board = minimax(board, 9, computer_letter, player_letter, True, -100, 100)
        visualise_board(board)


        if winning_condition(board,computer_letter):
            print("You loose")
            game_is_on = False
        elif full_board(board):
            print("That's a tie. Well played!")
            game_is_on = False

        else:
            turn = "player"
        """
        if winning_condition(board,computer_letter):
            print("Computer has won!")
            game_is_on = False
        else:
            if full_board(board):
                print("That's a tie. Well played!")
                game_is_on = False
                break

            else:
                turn = "player"
                """



