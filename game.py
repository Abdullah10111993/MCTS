from util import node, edge_move
from MCTS import MCTS
# def non_terminal(state):
# 	return (-1 in state)

# def fully_expanded(node):
# 	for edge in node.edges:
# 		if edge.visits == 0:
# 			return False
# 	return True

# def pick_univisted(node):
# 	for edge in node.edges:
# 		if edge.visits == 0:
# 			return edge
# 	return False

# def best_uct(node):
# 	best_winrate = 0
# 	best_edge = 0
# 	for edge in node.edges:
# 		if edge.visits != 0:
# 			winrate = edge.wins/edge.visits
# 		else:
# 			winrate = 0
# 		if winrate > best_winrate:
# 			best_edge = edge
# 			best_winrate = winrate
# 	if best_edge == 0:
# 		return random.choice(node.edges)
# 	return best_edge

# def traverse(node):
#     if fully_expanded(node):
#     	return best_uct(node)
#     else:
#     	return pick_univisted(node)  # in case no children are present / node is terminal 

# def generate_moves(state):
# 	possible_moves = []
# 	for i in range(len(state)):
# 		if state[i] == -1:
# 			possible_moves.append(i)
# 	return possible_moves

# def rollout_policy(state):
# 	moves = generate_moves(state)
# 	return random.choice(moves)

# def check_win(board):
# 	if board[0] == board[1] and board[1] == board[2]:
# 		return board[0]
# 	elif board[3] == board[4] and board[4] == board[5]:
# 		return board[3]
# 	elif board[6] == board[7] and board[7] == board[8]:
# 		return board[6]
# 	elif board[0] == board[3] and board[3] == board[6]:
# 		return board[0]
# 	elif board[1] == board[4] and board[4] == board[7]:
# 		return board[1]
# 	elif board[2] == board[5] and board[5] == board[8]:
# 		return board[2]
# 	elif board[2] == board[4] and board[4] == board[6]:
# 		return board[2]
# 	elif board[0] == board[4] and board[4] == board[8]:
# 		return board[0]
# 	else:
# 		if -1 in board:
# 			return -1
# 		else:
# 			return 2

# def result(state, player):
# 	win = check_win(state)
# 	return int(win == player)

# def make_move(move, player, state):
# 	state[move] = player

# def rollout(edge,board_state):
# 	player = edge.player
# 	new_board_state = board_state.copy()
# 	make_move(edge.move, player, new_board_state)
# 	player = 1 - player
# 	edge.visits += 1
# 	while non_terminal(new_board_state):
# 		move = rollout_policy(new_board_state)
# 		make_move(move,player,new_board_state)
# 		player = 1 - player
# 	return result(new_board_state, edge.player) 

# def backpropagate(edge, result):
# 	edge.wins += result

# def monte_carlo_tree_search(root, allowed_time):
# 	start = time.time()
# 	while time.time() - start <= allowed_time:
# 		edge = traverse(root) # edge = unvisited node 
# 		simulation_result = rollout(edge,root.board_state)
# 		backpropagate(edge, simulation_result)

# 	return best_uct(root)

mcts = MCTS()

def ai_play(board,ai_player):
	root = node(board,None,ai_player)
	edge = mcts.monte_carlo_tree_search(root,2)
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