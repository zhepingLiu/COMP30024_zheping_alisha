"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

class GameBoard:
    """
    GameBoard class that represents the game board of the game.
    GameBoard instance contains all valid positions (coordinates) on the game
    board.
    """
    def __init__(self):
        """
        Initialise a GameBoard instance. 
        Generate a list of all valid coordinates on the game board.
        """
        ran = range(-3, 4)
        self.game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

    def get_game_board(self):
        """
        Get all valid coordinates on the game board
        """
        return self.game_board

    def next_to(self, position_1, position_2):
        """
        Check if two positions are next to each other on the hex game board
        Input: position_1: the first given position
               position_2: the second given position
        Output: True if they are next to each other, otherwise False
        """
        HEX_STEPS = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
        (q1, r1) = position_1
        (q2, r2) = position_2

        for step_q, step_r in HEX_STEPS:
            if (q1 + step_q, r1 + step_r) == (q2, r2):
                return True

        return False

    def jump(self, position_1, position_2):
        """
        Compute the jump destination of one piece jump over another one
        Input: position_1: the coordinate of the given piece
               position_2: the coordinate of the given jump median
        Output: a tuple with a bool value and a possible coordinate or None;
                if the jump action is valid, return (True, jump_destination);
                otherwise, return (False, None)
        """
        SENTINEL = -4
        (q1, r1) = position_1
        (q2, r2) = position_2
        q = SENTINEL
        r = SENTINEL
        if q1 == q2 and r1 - r2 == 1:
            q = q1
            r = r2 - 1
        elif q1 == q2 and r1 - r2 == -1:
            q = q1
            r = r2 + 1
        elif r1 == r2 and q1 - q2 == 1:
            q = q2 - 1
            r = r1
        elif r1 == r2 and q1 - q2 == -1:
            q = q2 + 1
            r = r1
        elif q1 - q2 == -1 and r1 - r2 == 1:
            # e.g. (-1,0) and (0,-1)
            q = q1 + 2
            r = r1 - 2
        elif r1 - r2 == -1 and q1 - q2 == 1:
            # e.g. (2,1) and (1,2)
            q = q1 - 2
            r = r1 + 2

        # check if the generated position is a valid coordinate
        if (q, r) in self.get_game_board():
            return (True, (q, r))

        # when the tile is out of range, return None
        return (False, None)

    def get_jump_median(self, position_1, position_2):
        """
        Compute the jump median position between jump starting position and
        jump destination (if the jump is valid).
        Input: position_1: jump starting position
               position_2: jump destination
        Output: if the jump action is valid, return the coordinate of the 
                jump median; otherwise return False
        """
        (q1, r1) = position_1
        (q2, r2) = position_2
        q = None
        r = None

        if q1 == q2 and r1 - r2 == 2:
            q = q1
            r = r1 - 1
        elif q1 == q2 and r1 - r2 == -2:
            q = q1
            r = r1 + 1
        elif r1 == r2 and q1 - q2 == 2:
            q = q1 - 1
            r = r1
        elif r1 == r2 and q1 - q2 == -2:
            q = q1 + 1
            r = r1
        elif q1 - q2 == -2 and r1 - r2 == 2:
            # e.g. (-1,0) and (1,-2)
            q = q1 + 1
            r = r1 - 1
        elif q1 - q2 == 2 and r1 - r2 ==-2:
            # e.g. (2,1) and (0,3)
            q = q1 - 1
            r = r1 + 1

        if q != None and r != None:
            return (q, r)  
        else:
            return False

    def no_jump_for_enemy(self, game_state, my_piece, enemy_piece):
        """
        Check if the position of my_piece cannot be acquired by enemy pieces.
        There are three situations that it cannot be acquired by enemies:
        - First, the jump destination for the enemy piece is occupied by one of
          my piece;
        - Second, the jump destination for the enemy piece is occupied by one of
          their piece (same enemy for both jump starting position and 
          destination);
        - Thirdly, the jump destination is not an valid coordinate.

        Input: game_state: the given game_state
               my_piece: my piece that are possible to be captured
               enemy_piece: the enemy piece that are possible to capture
                            my piece
        
        Output: True if the enemy cannot acquire my piece;
                False otherwise
        """
        colour = game_state.get_colour(my_piece)
        jump_result = self.jump(enemy_piece, my_piece)
        # when jump destination is one of my pieces or one of their pieces,
        # if its my pieces, it can only be moved by me; if its their pieces,
        # they can only move one piece at each turn.
        if jump_result[0] == True and \
            (jump_result[1] in game_state.get_pieces(colour) or
             game_state.same_colour(jump_result[1], enemy_piece)):
            return True
        # when JUMP destination is out of the game board
        elif jump_result[0] == False:
            return True
        
        return False

    def manhattan_distance(self, position, colour):
        """
        Compute the manhattan distance from a piece to its closest goal on
        the hex game board
        Input: position: the coordinate of a piece
               colour: the colour of the given piece
        Output: the shortest distance between the piece and the goal
        """
        if colour == "red":
            goal = [[3, -3], [3, -2], [3, -1], [3, 0]]
        elif colour == "green":
            goal = [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
        elif colour == "blue":
            goal = [[0, -3], [-1, -2], [-2, -1], [-3, 0]]

        dist0 = (abs(position[0] - goal[0][0]) + abs(position[0] + position[1]
                - goal[0][0] - goal[0][1]) + abs(position[1] - goal[0][1])) / 2

        # take the minimum distance from distances to all goals
        for i in range(1, 4):
            temp_dist = (abs(position[0] - goal[i][0]) + abs(position[0]
                        + position[1] - goal[i][0] - goal[i][1]) +
                         abs(position[1] - goal[i][1])) / 2
            if temp_dist < dist0:
                dist0 = temp_dist

        return int(dist0)

    def hex_distance(self, position_1, position_2):
        """
        Compute the hex distance between any two valid coordinates.
        Input: position_1: the first given position
               position_2: the second given position
        Output: the distance between the two given position
        """
        dist = (abs(position_1[0] - position_2[0]) + abs(position_1[0] +
                   position_1[1] - position_2[0] - position_2[1]) +
                   abs(position_1[1] - position_2[1])) / 2

        return dist