from TicTac import *

class Q_Model():
	def __init__(self):
		self.table=create_Q_table()
		self.lr = .9 # learning rate. How much new info overides old
		self.dr = .9 # discount rate. Determines importance of future moves
		self.rf = .9 # randomness factor. [ RANDOM (0.0) to NOT Random (1.0)]

	def train(self,data,p_sym):
		"""runs training on one dataset in the POV og p_sym"""
		status = data[0]
		positions = data[1:]
		if p_sym !=1:
			data = [compliment(ix) for ix in positions]

		for i in range(len(positions)-1):
			next_pos = positions[-i]
			prev_pos = positions[-(i+1)]
			if type(self.table[next_pos])==dict():
				next_max = max(self.table[next_pos].values())
				prev_value = self.table[prev_pos] 
				prev_value = prev_value + self.lr*(self.table[prev_pos][next_pos] + self.dr*next_max - prev_value)

def create_Q_table():
	'''recursively creates future possbiel board configurations: where p1 or p2 starts first
	{
	tup1:{tupa:Q,
	 	  tupb:Q},
	tup2:{tupc:Q,
	 	  tupd:Q}	 
	}
	'''
	
	count = 0
	def helper():
		"""recursive creates as possible 1,2,0 combo"""
		nonlocal count
		if count == 8:
			return [[0],[1],[2]]
		else:
			count+=1
			result = []
			Recur = helper()
			for i in Recur:
				result.append(i+[0])
				result.append(i+[1])
				result.append(i+[2])
			return result
	# call recursive create
	sorted_poss = set()
	all_poss = helper()

	#filer out invalid boards
	for board in all_poss:
		if is_legal(board) and not (is_win(board,1) and is_win(board,2)):
			sorted_poss.add(tuple(board))
	# initialize Q table with random ints as Q values
	Q_table =dict()
	for board in sorted_poss:
		### SCORING BOARDS #########
		p1_wins = (is_win(board,1))
		p2_wins = (is_win(board,2))
		if (not (p1_wins or p2_wins)) and (0 not in board): # TIEs
			Q_table[board] = 50
		elif p1_wins:	  									# WINNING BOARDS
			Q_table[board] = 100
		elif p2_wins:
			Q_table[board] = -100							# LOSING BOARDS
		else:					  							# OTHER
			all_next_boards=[]
			if board not in Q_table:
				Q_table[board] = dict()
			for player in curr_move(board):
				for place in range(len(board)):
					if board[place] == 0:
						next_board = list(board)
						next_board[place] = player
						all_next_boards.append(tuple(next_board))

			# create a next_B --> Qvalue map 
			for next_B in all_next_boards:
				Q_table[board][next_B] = random.uniform(-.5,.5) ## initailize Q value to a number between -1 and 1
		########################################
	return Q_table

Q=Q_Model()
print(Q.table)
X_win=["X", (0, 0, 0, 0, 0, 0, 0, 1, 0), (0, 2, 0, 0, 0, 0, 0, 1, 0), (0, 2, 0, 0, 0, 0, 1, 1, 0), (2, 2, 0, 0, 0, 0, 1, 1, 0), (2, 2, 0, 0, 0, 1, 1, 1, 0), (2, 2, 0, 0, 2, 1, 1, 1, 0), (2, 2, 1, 0, 2, 1, 1, 1, 0), (2, 2, 1, 2, 2, 1, 1, 1, 0), (2, 2, 1, 2, 2, 1, 1, 1, 1)]
#a = Q.train(X_win,1)
#b = Q.train(X_win,2)
#print(a)
for item in Q.table.values():
	print(type(item))
	if type(item) == int:
		print(item)