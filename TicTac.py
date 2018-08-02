import random

def is_win(board,player_num):
	"""
	args: given board state in 1 and 2 and 0
	player_num: the number on the board that refers to the player

	returns True if wins, False if loses"""
	# covert to complement if player 2
	if player_num == 2:
		board = tuple([2 if i == 1 else 1 if i ==2 else 0 for i in board])
	# run checks
	zero = board[0];one = board[1];two = board[2];three = board[3];four = board[4];five = board[5];six = board[6];seven = board[7];eight = board[8]
	# middle wins
	if four == 1:
		# horizontals
		if ((one,seven) == (1,1)) or ((three,five)==(1,1)):
			return True
		#diagonals
		if ((zero,eight)==(1,1)) or ((two,six)==(1,1)):
			return True
	#top left corver
	if zero == 1:
		if ((three,six)==(1,1)) or ((one,two)==(1,1)):
			return True
	#bottom rgiht corners
	if eight == 1:
		if ((six,seven)==(1,1)) or ((two,five)==(1,1)):
			return True
	return False

def is_ongoing():
	pass

def is_legal(board):
	num_1 = board.count(1)
	num_2 = board.count(2)
	if abs(num_1 - num_2) <=1:
		return True
	else: 
		return False
def curr_move(board):
	"who is moving next"
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





#print(create_Q_table())
class Player():
	def __init__(self,name,sym,num,score = 0):
		self.name = name
		self.sym = sym
		self.score = score
		self.num = num

	def __str__(self):
		return self.sym
def set_board(board,position,new_value):
	board = list(board)
	board[position] = new_value
	return tuple(board)


class Game():
	'''handles scores, human input mode, game history, who is playing now?, current tabel, visualiztion'''
	def __init__(self, p1_name = "cpu_1", p2_name = "cpu_2"):
		self.board = (0,)*9
		self.count = 0
		self.history = ["ongoing"] # list of game boards. first index = game_state ("ongoing": ongoing, "tie": tie, p1.sym: p1_win, p2.sym: p2_wins)
		self.all_history=[] # list of 
		self.p1 = Player(p1_name,"X",1)
		self.p2 = Player(p1_name,"O",2)
		self.state ="ongoing"
		self.priority = int(self.p1.num)


	def reset(self):
		self.board = (0,)*9
		self.all_history.append(self.history)
		self.count +=1
		self.history = ["ongoing"]
		#self.p1 = Player(p1_name,"X",1)
		#self.p2 = Player(p1_name,"O",2)
		self.state ="ongoing"
		self.priority = int(self.p1.num)


	def check_end_game(self):
		'''Checks if game ended. if so, set self. state = whoever wins
		return True if over, 
		False if not'''
		#print("checked end is called" ,self.board,2,is_win(self.board,self.p2.sym))
		if is_win(self.board,self.p1.num):
			self.state = str(self.p1.sym) + " wins"
			self.p1.score+=1
			self.history[0] = self.p1.sym
			return True
		elif is_win(self.board,self.p2.num):
			print("p2 won",self.state)
			self.state = str(self.p2.sym) + " wins"
			self.p2.score+=1
			self.history[0] = self.p2.sym
			return True
		elif 0 not in self.board:
			self.state = "tie"
			self.p1.score+=1
			self.p2.score+=1
		else:
			self.state = "ongoing"
			return False



	def __str__(self):
		disp = "_____________________________________\n"
		indent = "  "
		disp += " TIC-TAC-TOE\n\n"+indent
		## make pices
		
		count = 0
		for piece in self.board:
			if self.p1.num == piece:
				char = self.p1.sym  
			elif self.p2.num == piece:
				char = self.p2.sym
			else:
				char = " "
			if count in {2,5}:
				char += "\n"+indent+"=========\n"+indent
			if count in {0,3,6,1,4,7}:
				char+=" | "
			count+=1
			disp+=char
		## display state
		disp+= "\n\nStatus: " + str(self.state) 
		if self.state !="ongoing": 
			disp += "  Enter any key to reset game"
		## disp scores
		disp+= "\nPlayer_1("+self.p1.sym+"): " + str(self.p1.score)+"\nPlayer_2("+self.p2.sym+"): "+str(self.p2.score)+"\n"
		disp+= "Current Move: " + str(["Player 1\n" if self.p1.num == self.priority else "Player 2\n" if self.p2.num == self.priority else "\n"][0])
		disp+= "Enter [end] to end session\n"

		return disp

	def step(self,place):
		'''see who shoudl be currently moving. based on Q values, make move, set new Q values. '''
		
		if self.state == "ongoing":
			## set the piece
			# if player one		
			if self.p1.num == self.priority:
				if self.board[place] == 0:
					new_board = set_board(self.board,place,self.p1.num)
					if new_board != self.board:
						self.history.append(new_board)
						self.priority = self.p2.num
					

			## if plater 2
			elif self.p2.num == self.priority:
				if self.board[place] == 0:
					new_board = set_board(self.board,place,self.p2.num)
					if new_board != self.board:
						self.history.append(new_board)
						self.priority = self.p1.num

			self.board = new_board
			self.check_end_game()
				
		else:
			self.reset()



		

def pvp():
	""" player vs player game"""
	g=Game()
	print(g)
	n = None
	while True:

		try:
			n = input()
			if n == "end":
				return False
			n = int(n)
			g.step(n)
		except:
			pass

		print(g.history)
		print(g)

def future_max():
	''' finds the highest possible score based on next few moves'''
	def front_prop():
		'''recursive func that find 
		your move: maximizes your score,
			enmy move: minimizes your score
				RECUR! : recursive call to find the next best move 
		select the max
		'''
		pass
	pass
if __name__ == "__main__":
	pvp()
	#print(is_win((2,2,2,0,1,0,1,1,0),2))

