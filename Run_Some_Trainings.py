from TicTac import *
from TTT_Q_learning import *
import pickle
import random
import matplotlib.pyplot as plt
import pickle
import time
from API_TTT import *

#import pandas
#import matplotlib.pyplt as plt
Desktop=""
f_name ="Q_table_After_delete.pkl"

def pickle_save(item):

    """saves data to a pickle file located on the desktop"""
    with open(f_name,'wb') as f:  # Python 3: open(..., 'rb')
        pickle.dump(item, f)# Save a dictionary into a pickle file.
        print("data saved to ",f_name)

def pickle_load(filename=f_name):
    """loads data from a desktop pickle file. returns the data"""
    with open(filename,'rb') as f:  # Python 3: open(..., 'rb')
        loaded = pickle.load(f)
        print("loaded data from: ",filename)
    return loaded
def plot_history(Scores):
    X=[]
    y1=[]
    y2=[]
    y3=[]
    y4=[]
    Model_Pts = 0
    API_Pts = 0
    for item in Scores:
        X.append(item)
        vals = list(Scores[item].values())
        y1.append(vals[0])
        y2.append(vals[1])
        Model_Pts+=vals[0]
        API_Pts+=vals[1]
        y3.append(Model_Pts/item)
        y4.append(API_Pts/item)
    plt.plot(X, y1, 'r--',label='MODEL: p1')
    plt.plot(X, y2, 'b--',label='API p2')
    plt.plot(X, y3, 'g--',label='Model_Pts/Epoch')
    plt.plot(X, y4, 'y--',label='API_Pts/Epcoh')
    plt.legend()
    plt.show()

# run trainings 
# 1. Create Game
# 2. Play ten games
# 3. Run trainin gusing history of the ten games
# 4. Test the model on random play. Play about 100 games and see result
# 5. Store the game results.
# 6. Reinitialize Game
# 7. Repeat for n interations

#Q=pickle_load(filename)

def run_train():
    Q=pickle_load()
    #Q= Q_Model()
    print(Q)
    EPOCHS = 600
    Scores = {}
    for EPOCH_num in range(1,EPOCHS):
        print(EPOCH_num)
        # initialize each game
        
        g = Game()
        total_games = 0
        # play ten games
        t=time.time()
        while total_games < 40:

            total_games +=1
            #Rand_vs_Rand(g)
            while g.state == "ongoing":
                if g.priority == g.p2.num:
                    API_step(g,.9)
                    #Model_Step(g,Q)
                elif g.priority == g.p1.num:
                    Model_Step(g,Q)
                else:
                    pass
            g.step("new_game")
            hist = g.all_history
            h = hist[-1]
            Q.train(h,"X")
            Q.train(h,"O")
        print("Time: ",time.time()-t)
        pickle_save(Q)
            
        Scores[EPOCH_num] = g.score
    print(Scores)
    plot_history(Scores)
    pickle_save(Q)

def test_single_game():
    Q=pickle_load(filename = f_name)

    history = [{'X': 1, 'O': 2, 'result': 2}, (0, 0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 1, 0, 0, 0, 0), (2, 0, 0, 0, 1, 0, 0, 0, 0), (2, 0, 0, 1, 1, 0, 0, 0, 0), (2, 0, 0, 1, 1, 2, 0, 0, 0), (2, 0, 0, 1, 1, 2, 1, 0, 0), (2, 0, 2, 1, 1, 2, 1, 0, 0), (2, 0, 2, 1, 1, 2, 1, 1, 0), (2, 2, 2, 1, 1, 2, 1, 1, 0)]
    for i in range(1,len(history[1:])):
        print(i,Q.table[history[-(i+1)]][history[-i]])
    print("___________________________________")
    Q.train(history,"O")
    
    for i in range(1,len(history[1:])):
        print(i,Q.table[history[-(i+1)]][history[-i]])

if __name__ == "__main__":
    run_train()


