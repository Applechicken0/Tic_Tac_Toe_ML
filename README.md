# Tic_Tac_Toe_ML
Create a TicTacToe Game and AI using machine learning

### Overview

The fact that machine learning is able master complicated games like chess is just really amazing, and I wanted to learn how to do that.  For the purpose of learning machine learning, I created a Tic Tac Toe environment to play the game, implemented a Q Learning Reinforcement Model, and trained the Model on my game!

### Game Environment
Creating, Managing, Logging, Playing and Visualizing Games of Tic Tac Toe
The code is found in TicTac.py

I implemented a class for my Tic Tac Toe Game that stored the important information about the game such as
* The Game State: ongoing, tie, player 1 wins or player 2 wins
* The Score
* The Game History: Stores the past game boards of multiple games and the outcome 
* Which Player's Turn to Move 
* The Board: A tuple with each index representing one of the 9 indexs of a game board, with values
** 0: Empty
** 1: Player 1
** 2: Player 2

These functions and methods to allow easy interfacing with the game
* step( ): Makes a move 
* str( ): Creates a visual representation of the board for visualization
* reset( ): Resets the game parameters to play another round of TicTicTac
* is_win( ): Checks if given the board postion, 
* check_end_game( ): Calls other functions to manage end game situations

Player Classes to Represent Player Entities and stores values such as
* Symbol
* Scores

## Learning Model
The Q table is represented as a the Q_Model( ) class. This class manages creating Q tables, updating Values and running Trainings.
The code is found in TTT_Q_learning.py

=



<img src = "Pictures/500_Zoom_Improvement.png">
