import requests
import json
from TicTac import *
from TTT_Q_learning import Rand_Step


def board_tup_to_str(board):
	result =""
	for i in board:

		if i ==0:
			n = "-"
		elif i==1:
			n="X"
		elif i==2:
			n="O"
		result+=n

	return result

def TTT_API_call(board,player_sym):
	board_str = board_tup_to_str(board)

	response = requests.get("https://stujo-tic-tac-toe-stujo-v1.p.mashape.com/"+board_str+"/"+player_sym,
	  headers={
	    "X-Mashape-Key": "29Pn8JXcWhmshoXRbwTEM3vKQR4zp1CiXkPjsnCLJ7EXqtluB9",
	    "Accept": "application/json"
	  }
	)
	j =response.json()
	if "recommendation" in j:
		
		return j["recommendation"]
	

def API_step(g,level = .8):
	r = random.uniform(0,1)
	if r > level:
		Rand_Step(g)
	else:
		if g.p1.num==g.priority:
			sym = g.p1.sym
		elif g.p2.num == g.priority:
			sym = g.p2.sym

		step_num = TTT_API_call(g.board,sym)
		if step_num == None:
			Rand_Step(g)
		else:
			g.step(step_num)



if __name__ == "__main__":
	pass
	#g = Game()
	'''while True:
		while g.state == "ongoing":
			API_step(g)
			print(g)
			print(g.state)
		g.step(0)'''