#Report
##Formulation of the game
###states : {current positions of all pieces, previous action to get to this state, current positions of all blocks, previous state, colour of the pieces}
###actions: include JUMP, MOVE, EXIT
###goal test: all pieces are removed from the game board
###sub goal: any piece is at the EXIT positions
###path cost: simply assuming the cost of each action is 1

##Search Algorithm
###A_star
###Modified manhattan distance for hex board
###The heuristic is the sum of the distance from all pieces to their closest EXIT position

##Time complexity and space complexity
###Space complexity is very high due to the structure of the state, i.e. a dict contains all previous states from the start state
###Time complexity???

###The states of the game is structured as a dictionary with elements {current positions of all pieces, previous action to get to this state, current positions of all blocks, previous state, colour of the pieces}. The actions include JUMP, MOVE, and EXIT. The goal test is achieved by testing if all pieces are removed from the game board. As the final goal requires an extra step from the EXIT position, the sub goal is for any piece to get to the EXIT position. The path cost for each action is simply assumed as 1 in this program. 

###The search algorithm used by the program is A*, with the modified  Manhattan distance for hexagonal grids. This algorithm is chosen for the optimality and relatively short time consumption. The time complexity for A * search is exponential in (relative error in the heuristic x length of solution). This algorithm is also complete, unless there are infinitely many nodes with f <= f(G), which does not appear in this program. The space required for A * search is to keep all nodes in memory. The modified Manhattan distance heuristic is admissible as it is the sum of the distance from all pieces to their closest EXIT positions respectively. The states to be visited are stored in a priority queue, which takes the shortest heuristic distance as priority to achieve uniform cost search. 

###The space complexity for this program is very high due to the structure of “states”. “States” is a dictionary with one of the elements being previous state. Previous state stores all “states” dictionaries before the current action, therefore, accumulates magnificently as more actions are taken. 