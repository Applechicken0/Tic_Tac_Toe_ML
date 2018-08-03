import random

def compliment(board):
	""" given tuple of 0,1,2' replaces 2 with 1 and 1 with 2's"""
	board = tuple([2 if i == 1 else 1 if i ==2 else 0 for i in board])
	return board

def is_win(board,player_num):
	"""
	args: given board state in 1 and 2 and 0
	player_num: the number on the board that refers to the player

	returns True if wins, False if loses"""

	# covert to complement if player 2
	if player_num == 2:
		#board = tuple([2 if i == 1 else 1 if i ==2 else 0 for i in board])
		board = compliment(board)
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

def is_tie():
	
	pass


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
		self.p1 = Player(p1_name,"X",1)
		self.p2 = Player(p1_name,"O",2)
		self.history = [{self.p1.sym:self.p1.num,self.p2.sym:self.p2.num,"result":"ongoing"},self.board] # list of game boards. first index maps player anme with player num and stores game state ,game_state ("ongoing": ongoing, "tie": tie, p1.sym: p1_win, p2.sym: p2_wins)
		self.all_history=[] # list of 
		self.state ="ongoing"
		self.priority = int(self.p1.num)


	def reset(self):
		""" sets the game to initial start state. Allows mutiple games to be played in one session """
		self.board = (0,)*9
		self.all_history.append(self.history)
		self.count +=1
		self.history = ["ongoing"]
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
			self.history[0]["result"] = self.p1.num
			return True
		elif is_win(self.board,self.p2.num):
			self.state = str(self.p2.sym) + " wins"
			self.p2.score+=1
			self.history[0]["result"] = self.p2.num
			return True
		elif 0 not in self.board:
			self.state = "tie"
			self.p1.score+=1
			self.p2.score+=1
			self.history[0]["result"] = "tie"
		else:
			self.state = "ongoing"
			return False



	def __str__(self):
		""" creates a display of the tic tav toe board and relevent information to play"""
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
	while g.state == "ongoing":

		try:
			#n = input()
			n = random.choice((0,1,2,3,4,5,6,7,8,9))
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

