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