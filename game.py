import time
import random

class node:
	def __init__(self,state,parent,player):
		self.board_state = state
		self.parent = parent
		self.children = []
		self.is_visitted = False
		self.vists = 0
		self.wins = 0
		self.ai_player = player
		self.player = player

	def generate_children(self):
		for i in range(len(self.board_state)):
			copy = self.board_state.copy()
			if self.board_state[i] == -1:
				copy[i] = 1 if self.player == 1 else 0
				child_player = 0 if self.player == 1 else 1
				self.children.append(node(copy,self,child_player))

def non_terminal(node):
	if -1 in node.board_state:
		return True
	else:
		return False

def fully_expanded(node):
	for c in node.children:
		if c.is_visitted == False:
			return False

def pick_univisted(node):
	for c in node.children:
		if c.is_visitted == False:
			return c
	return False

def best_uct(node):
	best_winrate = 0
	best_node = 0
	for c in node.children:
		if c.vists != 0:
			winrate = c.wins/c.vists
		else:
			winrate = 0
		if winrate > best_winrate:
			best_node = c
			best_winrate = winrate
	if best_node == 0:
		return random.choice(node.children)
	return best_node

def traverse(node):
    while fully_expanded(node):	
        node = best_uct(node)
    n = pick_univisted(node) 
    if n:
    	return n
    else:
    	return node # in case no children are present / node is terminal 

def rollout_policy(node):
	node.generate_children()
	return random.choice(node.children)

def check_win(board):
	if board[0] == board[1] and board[1] == board[2]:
		return board[0]
	elif board[3] == board[4] and board[4] == board[5]:
		return board[3]
	elif board[6] == board[7] and board[7] == board[8]:
		return board[6]
	elif board[0] == board[3] and board[3] == board[6]:
		return board[0]
	elif board[1] == board[4] and board[4] == board[7]:
		return board[1]
	elif board[2] == board[5] and board[5] == board[8]:
		return board[2]
	elif board[2] == board[4] and board[4] == board[6]:
		return board[2]
	elif board[0] == board[4] and board[4] == board[8]:
		return board[0]
	else:
		if -1 in board:
			return -1
		else:
			return 2

def result(node):
	win = check_win(node.board_state)
	if win == node.ai_player:
		return 1
	else:
		return 0

def rollout(node):
	while non_terminal(node):
		node = rollout_policy(node)
	return result(node) 

def backpropagate(node, result):
	if node.parent == None:
		return
	node.wins += result
	node.vists += 1 
	backpropagate(node.parent, result)

def monte_carlo_tree_search(root, allowed_time):
	start = time.time()
	i=0
	while time.time() - start <= allowed_time:
		leaf = traverse(root) # leaf = unvisited node 
		simulation_result = rollout(leaf)
		backpropagate(leaf, simulation_result)
		# for c in root.children:
		# 	print(c.wins)
		# 	print(c.vists)
	return best_uct(root)

def ai_play(board,ai_player):
	root = node(board,None,ai_player)
	child = monte_carlo_tree_search(root,5)
	return child.board_state

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
# while True:
# 	printBoard(tictacBoard)
# 	player_input = int(input(str(turn)+" turn. Input Position: "))
# 	tictacBoard[player_input-1] = turn_dict[turn]
# 	win = check_win(tictacBoard)
# 	if win == 2:
# 		print("its a draw")
# 		break
# 	elif win == 1:
# 		print("X Won!!!")
# 		break
# 	elif win == 0:
# 		print("O Won!!!")
# 		break
# 	turn = 'O' if turn == 'X' else 'X'
printBoard(tictacBoard)
while True:
	player_input = int(input("Input Position: "))
	tictacBoard[player_input-1] = letter_map[user]
	printBoard(tictacBoard)
	win = check_win(tictacBoard)
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
	win = check_win(tictacBoard)
	if win == 2:
		print("its a draw")
		break
	elif win == 1:
		print("X Won!!!")
		break
	elif win == 0:
		print("O Won!!!")
		break