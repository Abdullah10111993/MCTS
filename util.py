class node:
	def __init__(self,state,parent, player):
		self.board_state = state
		self.parent = parent
		self.edges = []
		self.create_edges(player)
	
	def create_edges(self, player):	
		for i in range(len(self.board_state)):	
			if self.board_state[i] == -1:
				self.edges.append(edge_move(i,player))

	def rank_edges(self):
		pass
	


class edge_move:
	def __init__(self, move, player):
		self.move = move
		self.visits = 0
		self.wins = 0
		self.player = player
