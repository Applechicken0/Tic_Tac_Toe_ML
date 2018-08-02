from TicTac import *
#from TicTac import is_win
#from TicTac import is_legal
#from TicTac import curr_move
#import random


class Q_Model():
	def __init__(self):
		self.table=create_Q_table()

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
		# find possible next baords
		if (is_win(board,1) or is_win(board,2)):
			Q_table[board]=None
		else:
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
	return Q_table

Q=Q_Model()
print(Q.table)