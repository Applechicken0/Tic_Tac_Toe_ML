from TicTac import *
from TTT_Q_learning import *
import pickle
import random

# run trainings 
# 1. Create Game
# 2. Play ten games
# 3. Run trainin gusing history of the ten games
# 4. Test the model on random play. Play about 100 games and see result
# 5. Store the game results.
# 6. Reinitialize Game
# 7. Repeat for n interations
Q=Q_Model()
EPOCHS = 10
for EPOCH_num in range(EPOCHS):
	# initialize each game
	
	g = Game()
	total_games = 0
	# play ten games
	while total_games < 10:

		
		total_games +=1
		Rand_vs_Rand(g)
		
	hist = g.all_history
	for h in hist:
		Q.train(h,"X")
		Q.train(h,"O")
	
	
	g = Game(p1_name = "MODEL",p2_name="CPU")
	total_games=0
	while total_games < 10:
		total_games +=1
		Model_vs_Rand(g,Q)
		print(g.score)
		


