from TicTac import *

def is_legal(board):
	num_1 = board.count(1)
	num_2 = board.count(2)
	if abs(num_1 - num_2) <=1:
		return True
	else: 
		return False

def curr_move(board):
	"""who is moving next. based on the count of """
	moves=[]
	num_0 = board.count(0)
	num_1 = board.count(1)
	num_2 = board.count(2)
	if num_0 == 0:
		return []
	elif num_2 > num_1:
		return [1]
	elif num_1 > num_2:
		return [2]
	elif num_1 == num_2:
		return [1,2]
	else:
		return "Error: Can't tell who's move it is"


#############    Q CLASS     ###############################
class Q_Model():
	def __init__(self):
		self.table = self.create_Q_table()
		self.lr = .9 # learning rate. How much new info overides old
		self.dr = .9 # discount rate. Determines importance of future moves
		self.rf = .9 # randomness factor. [ RANDOM (0.0) to NOT Random (1.0)]

	def train(self,data,p_sym):
		"""runs training on one dataset in the POV on p_sym"""
		status = data[0]
		p_num = status[p_sym]
		positions = data[1:]
		if p_sym !=1:
			data = [compliment(ix) for ix in positions]

		for i in range(1,len(positions)):

			next_pos = positions[-i]
			prev_pos = positions[-(i+1)]
			
			## if next position is winning, reward = d[pos] 
			next_max = max(self.table[next_pos].values())

			## assign Rewards ##
			reward = 0
			# rewards = last move
			if i == 0:
				result = status["result"]
				if result == p_num:
					reward = 100
				elif result == p_num:
					rewward = -100
				elif result == "tie":
					result = 50
				else:
					reward = 0
			# else rewards = 0
			else:
				reward = 0
			#####
			
			prev_value = self.table[prev_pos][next_pos]
			print("________________________\n",prev_pos,next_pos,"\n",prev_value)
			prev_value = prev_value + self.lr*( reward + self.dr*next_max - prev_value)
			self.table[prev_pos][next_pos] = prev_value
######  END OF CLASS DEFINITIONS ############

	@staticmethod
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
				Q_table[board] = {board:50}
			elif p1_wins:	  									# WINNING BOARDS
				Q_table[board] = {board:100}
			elif p2_wins:
				Q_table[board] = {board:-100}							# LOSING BOARDS
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

if __name__ == "__main__":
	Q=Q_Model()
	#print(Q.table)
	print((0,0,0,0,0,0,0,0,0) in Q.table)
	X_win=[{'O': 2, 'result': 1, 'X': 1}, (0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0, 0, 0, 0), (0, 2, 0, 1, 0, 0, 0, 0, 0), (0, 2, 1, 1, 0, 0, 0, 0, 0), (0, 2, 1, 1, 0, 0, 0, 2, 0), (0, 2, 1, 1, 0, 1, 0, 2, 0), (0, 2, 1, 1, 0, 1, 0, 2, 2), (0, 2, 1, 1, 1, 1, 0, 2, 2)]
	t = 0
	while (t<10):
		t +=1
		a = Q.train(X_win,"X")
	#b = Q.train(X_win,2)
	print(a)
