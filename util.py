class node:
	def __init__(self, state, parent, player):
		self.board_state = state
		self.parent = parent
		self.player = player
		self.edges = []
		self.create_edges(player)
		self.rank_edges()
	
	def create_edges(self, player):	
		for i in range(len(self.board_state)):	
			if self.board_state[i] == -1:
				self.edges.append(edge_move(i,player))

	def rank_edges(self):
		position_rank = [3,2,3,2,4,2,3,2,3] # probability
		best_move = 0
		for i in range(len(self.edges)):
		    x = self.edges[i]
		    j = i - 1
		    while j >= 0 and position_rank[self.edges[j].move] < position_rank[x.move]:
		        self.edges[j+1] = self.edges[j]
		        j = j - 1
		    self.edges[j+1] = x

	# def print_edges(self):
	# 	edges = []
	# 	for e in self.edges:
	# 		edges.append(e.move)
	# 	print(edges)

class edge_move:
	def __init__(self, move, player):
		self.move = move
		self.visits = 0
		self.wins = 0
		self.child = None