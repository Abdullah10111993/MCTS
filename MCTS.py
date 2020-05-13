import time
import random
from util import node as Node
import math

class MCTS:
	def non_terminal(self, state):
		return (-1 in state)

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

	def c_puct(self, node, edge):
		N_s_b = 0
		p = [0.125,0.083,0.125,0.083,0.167,0.083,0.125,0.083,0.125]
		
		for e in node.edges:
			N_s_b += e.visits
		
		if N_s_b == 0 or edge.visits == 0:
			return p[edge.move]
		
		P_s_a = p[edge.move]
		Q_s_a = 0
		
		if edge.visits != 0:
			Q_s_a = edge.wins / edge.visits

		return Q_s_a + 4*P_s_a*(math.sqrt(N_s_b)/(1+edge.visits))


	def traverse(self, node):
		edge_puct = []
		for edge in node.edges:
			edge_puct.append(self.c_puct(node,edge))

		edge_index = edge_puct.index(max(edge_puct))
		node.edges[edge_index].visits += 1
		edge = node.edges[edge_index]
		if edge.child:
			edge, node = traverse(edge.child)
		return edge, node
	    
	def generate_moves(self, state):
		possible_moves = []
		for i in range(len(state)):
			if state[i] == -1:
				possible_moves.append(i)
		return possible_moves

	def rollout_policy(self, state):
		moves = self.generate_moves(state)
		position_rank = [3,2,3,2,4,2,3,2,3]
		best_move = moves[0]
		for i in range(1,len(moves)):
			if position_rank[moves[i]] > position_rank[best_move]:
				best_move = moves[i]
		return best_move 

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
		win = self.check_win(state)
		return int(win == player)

	def make_move(self, move, player, state):
		state[move] = player

	def rollout(self, edge, board_state, player, ai_player):
		local_player = player
		new_board_state = board_state.copy()
		self.make_move(edge.move, local_player, new_board_state)
		local_player = 1 - local_player
		while self.non_terminal(new_board_state):
			# print(new_board_state)
			move = self.rollout_policy(new_board_state)
			self.make_move(move, local_player, new_board_state)
			# print(new_board_state)
			local_player = 1 - local_player
			# input()
		return self.result(new_board_state, ai_player) 

	def addNode(self,node, edge): #change name
		if edge.visits >= 6:
			# print("adding")
			board_state = node.board_state.copy() 
			self.make_move(edge.move, node.player, board_state)
			edge.children = Node(board_state, node, 1-node.player)

	def backpropagate(self, node, result):
		if node.parent == None:
			return
		for edge in node.parent.edges:
			if edge.child.board_state == node.board_state:
				edge.wins += result
		self.backpropagate(node.parent, result)

	def print_tree(self,root):
		print("Board:",root.board_state)
		for edge in root.edges:
			print("Edge Move:",edge.move)
			print("Edge Wins:",edge.wins)
			print("Edge Visits:",edge.visits)
			# if edge.child:
			# 	self.print_tree(edge.child)

	def monte_carlo_tree_search(self, root, allowed_time):
		start = time.time()
		while time.time() - start <= allowed_time:
			edge, node = self.traverse(root) # edge = unvisited node 
			# print(edge.move)
			# print(node.board_state)
			simulation_result = self.rollout(edge, node.board_state, node.player, root.player) # after rollout add node to tree
			# print(simulation_result)
			# print(root.board_state)
			# input()
			self.addNode(node, edge) # add node for the edge
			# print(node.board_state)
			# input()
			edge.wins += simulation_result
			self.backpropagate(node, simulation_result) 
			# print(node.board_state)
			# input()
		self.print_tree(root)
			# input()
		edge_puct = []
		for edge in node.edges:
			edge_puct.append(self.c_puct(node,edge))
		edge_index = edge_puct.index(max(edge_puct))
		return node.edges[edge_index]