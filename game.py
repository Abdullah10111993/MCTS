from util import node
from MCTS import MCTS

mcts = MCTS()

def ai_play(board,ai_player):
	root = node(board,None,ai_player)
	# print(root.board_state)
	edge = mcts.monte_carlo_tree_search(root,0.5)
	# print(root.board_state)
	mcts.make_move(edge.move, ai_player, root.board_state)
	return root.board_state

def printBoard(board):
	for i in range(1,10):
		if i%3 ==0:
			if board[i-1] == -1:
				print(" ")
			elif board[i-1] == 1:
				print("X")
			elif board[i-1] == 0:
				print("0")
		else:
			if board[i-1] == -1:
				print(" ",end="|")
			elif board[i-1] == 1:
				print("X",end="|")
			elif board[i-1] == 0:
				print("O",end="|")


letter_map = {'X' : 1, 'O' : 0}
tictacBoard = [-1, -1, -1, -1, -1, -1, -1, -1, -1]
ai_player = 'X' 
user = 'O'

printBoard(tictacBoard)
while True:
	player_input = int(input("Input Position: "))
	tictacBoard[player_input-1] = letter_map[user]
	printBoard(tictacBoard)
	win = mcts.check_win(tictacBoard)
	if win == 2:
		print("its a draw")
		break
	elif win == 1:
		print("X Won!!!")
		break
	elif win == 0:
		print("O Won!!!")
		break
	
	tictacBoard = ai_play(tictacBoard, letter_map[ai_player])
	printBoard(tictacBoard)
	win = mcts.check_win(tictacBoard)
	if win == 2:
		print("its a draw")
		break
	elif win == 1:
		print("X Won!!!")
		break
	elif win == 0:
		print("O Won!!!")
		break