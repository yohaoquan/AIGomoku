# AIGomoku
A simple AI Gomoku player implementation utilizing Negamax and Alpha-Beta Pruning

<p align="center">
  <img width="204" alt="image" src="https://user-images.githubusercontent.com/16907613/212166047-7a1074a5-88e1-467e-867f-2d68a1aa52fa.png">
</p>

AI Gomoku is a program written in Python that allows a user to play a Gomoku game with an AI player. The goal is to create an AI program that could simulate the thought process of a real Gomoku player when they are playing a (Gomoku) game -- making knowledged decisions on what the next move is based on the situation.

It was obvious at the beginning that minimax will be used as the heuristic search method. But it is soon realized that a full-fledged minimax algorithm is not the most cost-effective since in this type(zero-sum) of board games, one player’s gain equals to the other player’s lost. The evaluation algorithm is optimized since no matter who is next to move, their score could be evaluated by the same procedure. This simplification is called Negamax.

Negamax is implemented for AI to evaluate the situation of the whole game. First, The scores of the whole board is calculated after a possible move. Then, the resulting board scores of all possible moves is calculated. After that, depending on the search depth set, this process is repeated a number of times based on the previously evaluated moves. After that, the final choice of move is selected by choosing the path that resulted in the highest final board score. In the process, alpha-beta pruning is used to prune out the branches that is clearly leading to a worse situation in order to improve efficiency of our program.
<p align="center">
  <img width="707" alt="image" src="https://user-images.githubusercontent.com/16907613/212166225-fcfc7426-3899-4175-a1ed-752f0cb76a5a.png">
  <img width="322" alt="image" src="https://user-images.githubusercontent.com/16907613/212166269-cfbfc210-e685-4506-888b-29e9ef737260.png">
</p>

While evaluating the scores of the board, the program also take notes of the lowest Beta value, the worst (for AI) possible score the opponent can produce by a move after our move. The higher the Beta value is, the worse our situation we could possibly get. When we are evaluating the next possible move, we compare the current Beta value. If our current beta value is larger than the lowest Beta value of the whole evaluation process, we would cut this branch as the opponent will most definitely choose this move in order to gain maxmium advantage. This saves computation times significantly.

In testing, this AI implementation would win some novice players when it’s search depth is set to 1 or 2, and some medium players when it’s increased to 3 or 4. Because of the limited timeframe allowed for optimization, the computation time it takes for our AI to make a decision basically rendered our game not enjoyable when the search depth is increased to 5 and above. But overall the program demonstrated a fair amount of intelligence while running. In the future, I plan to optimize our board evaluation to only update the scores of the points on the board that will be influenced by the move made. This should drastically increase the efficiency, then it is possible to increase the search depth without affect the playability of our game.
