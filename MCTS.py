class MCTS:
	def non_terminal(self, state):
		return (-1 in state)

	def fully_expanded(self, node):
		for edge in node.edges:
			if edge.visits == 0:
				return False
		return True

	def pick_univisted(self, node):
		for edge in node.edges:
			if edge.visits == 0:
				return edge
		return False

	def best_uct(self, node):
		best_winrate = 0
		best_edge = 0
		for edge in node.edges:
			if edge.visits != 0:
				winrate = edge.wins/edge.visits
			else:
				winrate = 0
			if winrate > best_winrate:
				best_edge = edge
				best_winrate = winrate
		if best_edge == 0:
			return random.choice(node.edges)
		return best_edge

	def traverse(self, node):
	    if fully_expanded(node):
	    	return best_uct(node)
	    else:
	    	return pick_univisted(node)  # in case no children are present / node is terminal 

	def generate_moves(self, state):
		possible_moves = []
		for i in range(len(state)):
			if state[i] == -1:
				possible_moves.append(i)
		return possible_moves

	def rollout_policy(self, state):
		moves = generate_moves(state)
		return random.choice(moves)

	def check_win(self, board):
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

	def result(self, state, player):
		win = check_win(state)
		return int(win == player)

	def make_move(self, move, player, state):
		state[move] = player

	def rollout(self, edge,board_state):
		player = edge.player
		new_board_state = board_state.copy()
		make_move(edge.move, player, new_board_state)
		player = 1 - player
		edge.visits += 1
		while non_terminal(new_board_state):
			move = rollout_policy(new_board_state)
			make_move(move,player,new_board_state)
			player = 1 - player
		return result(new_board_state, edge.player) 

	def backpropagate(self, edge, result):
		edge.wins += result

	def monte_carlo_tree_search(self, root, allowed_time):
		start = time.time()
		while time.time() - start <= allowed_time:
			edge = traverse(root) # edge = unvisited node 
			simulation_result = rollout(edge,root.board_state)
			backpropagate(edge, simulation_result)

		return best_uct(root)

	def ai_play(self, board,ai_player):
		root = node(board,None,ai_player)
		edge = monte_carlo_tree_search(root,5)
		make_move(edge.move, ai_player, root.board_state)
		return root.board_state