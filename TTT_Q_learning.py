from TicTac import *
import operator
import random


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
	def __init__(self, lr = .9, dr = .9, rf = .7 ):
		self.table = self.create_Q_table()
		self.lr = lr # learning rate. How much new info overides old
		self.dr = dr # discount rate. Determines importance of future moves
		self.rf = rf # randomness factor. [ RANDOM (0.0) to NOT Random (1.0)]

	def train(self,data,p_sym):
		"""runs training on one dataset in the POV on p_sym
		[{self.p1.sym:self.p1.num,self.p2.sym:self.p2.num,"result":"ongoing"},self.board]"""
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
			if i == 1:
				result = status["result"]
				if result == "tie":
					reward = 50
				elif not isinstance(result,int):
					pass
				elif result == p_num: ### result: player won
					reward = 100
				elif result != p_num: ### result: other won
					reward = -100
			# else rewards = 0
			else:
				#print("no Rewarding")
				reward = 0
			#####
			
			prev_value = self.table[prev_pos][next_pos]
			prev_value = prev_value + self.lr*( reward + self.dr*next_max - prev_value)
			self.table[prev_pos][next_pos] = prev_value


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
######  END OF CLASS DEFINITIONS ############
def Rand_vs_Rand(g):
	""" plays one round, start to finish of a random vs random algorutym"""

	while g.state == "ongoing":

		# make 1st move
		Rand_Step(g)

		if g.state != "ongoing": break;
		# make second move
		Rand_Step(g)
	g.step(0)
	return g.score

def Rand_Step(g):
	""" Takes a random Step"""
	possible_moves = open_moves(g.board)
	move = random.choice(tuple(possible_moves))
	g.step(move)

def Model_Step(g,Q,level = .9):
	""" Uses model Q to make a move on game g"""
	r = random.uniform(0,1)
	if r > level:
		Rand_Step(g)
	else:
		#next_moves = Q.table[g.board]
		#next_board = max(next_moves.items(), key=operator.itemgetter(1))[0]
		next_board = Max_Min(g.board,Q)

		place = [i for i in range(len(g.board)) if g.board[i] != next_board[i]]
		if len(place)==0:
			pass
		else:
			g.step(place[0])

def Max_Min(board,Q):
	next_moves = Q.table[board]
	next_board = max([Min(poss_board,Q) for poss_board in next_moves.keys()], key=operator.itemgetter(1))[0]
	return next_board
def Min(board,Q):
	next_boards = Q.table[board]
	next_min_value = min(next_boards.items())
	return next_min_value


def Model_vs_Rand(g,Q):
	while g.state == "ongoing":
		# make 1st move
		Model_Step(g,Q)
		if g.state != "ongoing": break;
		# make second move
		
		Rand_Step(g)
	g.step(0)
	return g.score


if __name__ == "__main__":
	from Run_Some_Trainings import pickle_load
	
	print("Loading Model")

	Q = pickle_load()


	g=Game()
	while True:
		while g.state == "ongoing":
			m=input()
			# make 1st move
			Model_Step(g,Q)
			print(g)
			if g.state != "ongoing": break;
			# make second move
			m=input()
			Model_Step(g,Q)
			print(g)
		g.step(0)

	
	