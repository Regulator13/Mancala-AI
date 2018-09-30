#Mancala AI
#By Isaiah Frey
#This program will play the user in a game of Mancala

#---------------------Libraries---------------------#

import time
import pdb
import timeit
import copy
from random import randint

#------------------Initializations------------------#

#Initialize the board (0 and 7 are the score cups, 1-6 are player 1's 8-13 are the AI's)
#All cups begin with 4 pieces
board = [4 for i in range(14)]
#But the scoring cups begin with 0
board[0] = 0
board[7] = 0
#Set a time delay for moving so users can see what's happening
DELAY = 1
#Choose who goes first
player_is_first = True
#Keep track of the turn
turn = 1

#Database dictionary
database = {7:{0: 11, 1: 8, 2: 11, 3: 11, 5: 8, 6: 11, 7: 9, 8: 12, 9: 11, 11: 8, 12: 8},
			8:{0: 11, 1: 8, 2: 11, 3: 11, 5: 8, 6: 8, 7: 9, 8: 12, 9: 11, 11: 11, 12: 11},
			9:{0: 11, 1: 8, 2: 11, 3: 11, 5: 8, 6: 11, 7: 9, 8: 12, 9: 11, 11: 11, 12: 11},
			10:{0: 11, 1: 8, 2: 11, 3: 11, 5: 8, 6: 11, 7: 9, 8: 12, 9: 11, 11: 11, 12: 11}}

#Player move dictionary
find_player_move = {(0,4,4):1, (5,0,4):2, (5,5,0):3, (5,5,5):5, (4,5,5):6,
					(0,5,5):7, (6,0,5):8, (6,6,0):9, (6,6,6):11, (5,6,6):12}

#-------------- Database Functions------------------#

#This function creates a database of best first moves for a given depth
def create_database(board, depth):

	#Initialize the database
	move_database = {}

	#Store initial board
	board_saved = copy.deepcopy(board)
	board_original = copy.deepcopy(board)

	#Start with the computer going first
	move_database[0] = find_best_move(board,depth)

	#Restore the board
	board = board_saved

	#Then add each of the player's 11 possible starting moves
	for move in [1,2,3,5,6]:
		board_saved = copy.deepcopy(board)
		player_move(board, move)
		move_database[move] = find_best_move(board,depth)
		board = board_saved

	player_move(board, 4)
	for move in [1,2,3,5,6]:
		board_saved = copy.deepcopy(board)
		player_move(board, move)
		move_database[6+move] = find_best_move(board,depth)
		board = board_saved

	#Restore the board one more time
	board = board_original
	print()
	print()
	print("DATABASE")
	print(move_database)
	print()
	print()
	return board




#---------------General Functions-------------------#

def print_board(board):

	#Find the number of digits in the player's score
	width = len(str(board[0])) + 1

	#Print markers for the player
	print(f"{'':{width + 1}}", end='')
	for i in range(1,7):
		print(i, end='  ')
	print("<--- Move number")

	#Print the player's score properly spaced
	print(f"{board[0]:<{width}}", end='')

	#Print the player's side
	for i in range(1,7):
		print(f"{board[i]:{2}}", end=' ')
	print()

	#Print the computer's side
	print(f"{'':{width}}", end='')
	for i in reversed(range(7,14)):
		print(f"{board[i]:{2}}", end=' ')
	print()
	print()

def player_turn(board):

	print("****Player's Turn****")
	print()
	bonus = True

	#While the bonus is True, let the player move again
	while(bonus):

		#Make sure the game isn't over
		game_end = check_game_end(board)
		if game_end:
			break
		if not game_end:

			#Get the player's move
			while(True):
				try:
					move = int(input("Please enter a the number of cup you'd like to move. "))
				except ValueError:
					print("Please enter a number!")
					continue
				if move >= 1 and move <= 6:
					if board[move] > 0:
						break
					else:
						print("That cup has no pieces! Choose again.")
						continue
				else:
					print("Please enter a number 1 to 6!")

			#Then make the player's move
			board, bonus = player_move(board,move)

			#Print out the board
			print_board(board)

			#Pause for delay
			time.sleep(DELAY)

	#Finally return the board
	return board

def player_move(board, move):

	#Reset the bonus
	bonus = False

	#Grab the pieces and empty the cup
	pieces = board[move]
	board[move] = 0
	destination = move-pieces

	#If the destination is out of index, put it back in range
	if destination < -14:
		destination += 14
	if pieces-move >= 7:
		if destination != -14:
			destination -= 1
		else:
			destination = 1

	#Place one piece in each cup going around
	for cup in reversed(range(destination, move)):
		#Unless if it's the opponents score cup
		if cup != 7 and cup != -7:
			board[cup] += 1

	
	#If the last cup was the player's score cup, set the bonus move to true
	if destination == 0:
		bonus = True

	#After the last drop, if there is only one piece in that cup, move it and the opposite cup to the player's score
	elif board[destination] == 1 and (destination <= 6 and destination >= 1) and board[14-destination] != 0:
		board[0] += (board[14-destination] + 1)
		board[destination] = 0
		board[14-destination] = 0

	#Return the board and if the player gets a bonus move
	return board, bonus

def check_game_end(board):

	#Initialize to false
	game_end = False

	#If the player has no pieces in it's field
	for cup in range(1,7):
		if board[cup] != 0:
			break
	else:
		game_end = True

	#Then check the computer's field
	for cup in range(8,13):
		if board[cup] != 0:
			break
	else:
		game_end = True

	#Return the result
	return game_end

#----------------Computer Functions-----------------#

def computer_turn(board, depth):

	print("****Computer's Turn****")
	print()
	bonus = True

	#While the bonus is True, let the computer move again
	while(bonus):

		#Make sure the game isn't over
		game_end = check_game_end(board)
		if game_end:
			break
		if not game_end:

			board_saved = copy.deepcopy(board)
			#Get the computer's move
			move = find_best_move(board, depth)
			board = board_saved
			#Then make the computer's move
			board, bonus = computer_move(board,move)

			#Print the computer's move for clarity
			print(f"The computer moved {14-move}")

			#Print out the board
			print_board(board)

			#Pause for delay
			time.sleep(DELAY)

	#Finally return the board
	return board

def computer_move(board, move):

	#Reset the bonus
	bonus = False

	#Grab the pieces and empty the cup
	pieces = board[move]
	board[move] = 0
	destination = move-pieces

	#If the destination is out of index, put it back in range
	if destination < -14:
		destination == 14
	if move-pieces <= 0:
		if destination != -14:
			destination -= 1
		else:
			destination = 1

	#Place one piece in each cup going around
	for cup in reversed(range(destination, move)):
		#Unless if it's the opponents score cup
		if cup != 0 and cup != -14:
			board[cup] += 1

	
	#If the last cup was the player's score cup, set the bonus move to true
	if destination == 7:
		bonus = True

	#After the last drop, if there is only one piece in that cup, move it and the opposite cup to the player's score
	elif board[destination] == 1 and (destination <= 13 and destination >= 8) and board[14-destination] != 0:
		board[7] += (board[14-destination] + 1)
		board[destination] = 0
		board[14-destination] = 0

	#Return the board and if the player gets a bonus move
	return board, bonus

def find_best_move(board, depth):

	#For higher depths, use the database for the first turn
	if depth > 6 and depth < 11:

		#First check to see if its the first turn
		if turn == 1:

			print("Database used")
			return database[depth][0]

		#Check if it's the second turn
		if turn == 2:

			print("Database used")
			try:
				return database[depth][find_player_move[tuple(board[1:4])]]
			except KeyError:
				print("Database use failed")
	
	#Set temporary best
	best = -1000

	#Set alpha and beta for alpha-beta pruning
	alpha = -1000
	beta = 1000

	#Make each legal move and evaluate
	for move in range(8,14):

		if board[move] != 0:

			#Save the current board state before anything happens
			board_top_saved = copy.deepcopy(board)

			#Make the move
			board, bonus = computer_move(board, move)
			###
			start_time = time.process_time()

			#Evaluate, starting with the player's next move, unless the computer got a bonus move
			if bonus:
				score = mini_max(board, depth, False, alpha, beta)
			else:
				score = mini_max(board, depth-1, True, alpha, beta)

			###
			end_time = time.process_time()
			print(f"Move {14-move} took {end_time-start_time} seconds and scored {score}.")

			#If the score is equal to the current best, give a 33% chance of changing to that one
			if score == best and randint(1,2) == 1:
				best = score
				best_move = move

			#If the score is greater than the current best, record that move
			if score > best:
				best = score
				best_move = move

			#Return the board back to its original state
			board = board_top_saved

	#Return the best move
	return best_move

def mini_max(board, depth, player_to_eval, alpha, beta):

	#Get the current score of the board
	score = eval_board(board)

	#If the game is over stop evaluating deeper
	game_end = check_game_end(board)
	if game_end or score > 24:
		return score

	#If the computer is not out of depth
	if depth >= 0:

		#If this move is not pruned by alpha-beta pruning
		if alpha < beta:

			#If it's the player's turn
			if player_to_eval:

				#Set a temporary best
				best = 1000

				#Then make all possible moves
				for move in range(1,7):
					if board[move] != 0:

						#Save the board state
						board_saved = copy.deepcopy(board)

						#Make the move
						board, bonus = player_move(board, move)

						#Evaluate
						if bonus:
							best = min(best, mini_max(board, depth, True, alpha, beta))
						else:
							best = min(best, mini_max(board, depth-1, False, alpha, beta))

						#Update the beta
						beta = min(beta,best)

						#Reset the board
						board = board_saved

				#Return the best score
				return best

			#If it's the computer's turn
			if not player_to_eval:

				#Set a temporary best
				best = -1000

				#Then make all possible moves
				for move in range(8,14):
					if board[move] != 0:

						#Save the board state
						board_saved = copy.deepcopy(board)

						#Make the move
						board, bonus = computer_move(board, move)

						#Evaluate
						if bonus:
							best = max(best, mini_max(board, depth, False, alpha, beta))
						else:
							best = max(best, mini_max(board, depth-1, True, alpha, beta))

						#Update the alpha
						alpha = max(alpha,best)

						#Reset the board
						board = board_saved

				#Return the best score
				return best

	return score

def eval_board(board):
	#pdb.set_trace()
	score = board[7] - board[0]
	###
	#print(f"Score is {score}")
	return score


#---------------------Main--------------------------#

if __name__ == '__main__':

	#Have the player decide the depth to which the computer will search each move
	while True:
		try:
			depth = int(input("Please input a depth for the computer searches (higher number = longer wait times). "))
		except ValueError:
			print("Please input an integer")
			continue
		if depth > 10 or depth < 0:
			print("Please input an integer from 0 to 10.")
			continue
		else:
			break

	#Uncomment the following line to create a data base of the depth entered in game
	#board = create_database(board,depth)

	while True:
		try:
			first = input("Would you like to go first? Enter y for yes or n for no. ")
		except:
			print("That is not a valid input.")
			continue
		if first.lower() == 'y':
			player_is_first = True
			break
		else:
			player_is_first = False
			break

	game_end = False
	print_board(board)

	#Main game loop
	while not game_end:

		if player_is_first:

			#Make the player's turn
			board = player_turn(board)
			#See if anyone won
			game_end = check_game_end(board)
			#Change turns
			player_is_first = not player_is_first
			turn += 1

		else:

			#Make the computer's turn
			board = computer_turn(board, depth)
			#See if anyone won
			game_end = check_game_end(board)
			#Change turns
			player_is_first = not player_is_first
			turn += 1

	#If someone won see who it was		
	if board[7] > board[0]:
		print("The computer won")
	elif board[0] > board[7]:
		print("You won!")
	else:
		print("It's a tie!")
	