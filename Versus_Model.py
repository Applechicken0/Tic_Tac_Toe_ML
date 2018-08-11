from TicTac import *
from TTT_Q_learning import *
from Run_Some_Trainings import *

print("Loading Model")
g = Game(p1_name = "Franklin", p2_name = "Model")
Frank=g.p1
Model=g.p2'

## loads a trained model 
Q = pickle_load(filename = "Saved_Models/Q_table_After_delete.pkl" ) #Trained Model
## To play a untrained model, comment out the above line and uncomment the below one
##Q = Q_Model() ## Untrained Model
####
print("Starting_Game")
while True:
	print(g)
	m = input()
	if m=="end":break;

	if g.state == "ongoing":
		if g.priority == g.history[0][Frank.sym]:
			try:
				m=int(m)
				g.step(m)
			except:
				pass
		elif g.priority == g.history[0][Model.sym]:
			Model_Step(g,Q)
	else:
		g.step(0)
	
