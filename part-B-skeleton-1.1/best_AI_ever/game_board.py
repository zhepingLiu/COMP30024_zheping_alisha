class GameBoard:
    def __init__(self):
        ran = range(-3, 4)
        self.game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

    """
    Get all valid coordinates on the game board
    """
    def get_game_board(self):
        return self.game_board

    """
    Check if two positions are next to each other on the hex game board
    Input: position_1: given position 1
           position_2: given position 2
    Output: True if they are next to each other, otherwise False
    """
    def next_to(self, position_1, position_2):
        HEX_STEPS = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
        (q1, r1) = position_1
        (q2, r2) = position_2

        for step_q, step_r in HEX_STEPS:
            if (q1 + step_q, r1 + step_r) == (q2, r2):
                return True

        return False

    """
    Generate the successor coordinate for a piece to JUMP through a block
    Input: position_1: the coordinate of the given piece
           position_2: the coordinate of the given jump median
    """
    def jump(self, position_1, position_2):
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

        # check if the generated position is in the valid range
        if (q, r) in self.get_game_board():
            return (True, (q, r))

        # when the tile is out of range, return empty
        return (False, None)

    def get_jump_median(self, position_1, position_2):
        # TODO: return the medium position between a jump action
        # Assumption: the jump action is valid
        SENTINEL = -4
        (q1, r1) = position_1
        (q2, r2) = position_2
        q = SENTINEL
        r = SENTINEL

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

        return (q, r)

    def distance_to_enemy_pieces(self, game_state):
        distances = {}
        my_pieces = game_state.get_my_pieces()
        enemy_pieces = game_state.get_enemy_pieces(game_state.colour)

        for my_piece in my_pieces:
            distances[my_piece] = {}
            for enemy_team in enemy_pieces.values():
                for enemy_piece in enemy_team:
                    distances[my_piece][enemy_piece] = self.hex_distance(
                                                       my_piece, enemy_piece)

        return distances

    def no_jump_for_enemy(self, game_state, my_piece, enemy_piece):
        jump_result = self.jump(enemy_piece, my_piece)
        # when JUMP destination for enemy_piece is my piece or => impossible
        # IF the piece belongs to the previous player, that player have opportunity
        # to eat my piece if the after_player moves their piece away
        if jump_result[0] == True and \
            jump_result[1] in game_state.get_my_pieces():
            return True
        # when JUMP destination is out of the game board
        elif jump_result[0] == False:
            return True
        
        return False

    # compute the manhattan distance from a piece to its closest goal on
    # the hex game board
    # Input: position: the coordinate of a piece
    #        colour: the colour of the input piece
    # Output: the shortest distance between the piece and the goal
    def manhattan_distance(self, position, colour):
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
        dist = (abs(position_1[0] - position_2[0]) + abs(position_1[0] +
                   position_1[1] - position_2[0] - position_2[1]) +
                   abs(position_1[1] - position_2[1])) / 2

        return dist
    
    def get_piece_colour(self, position):
        for colour in ["red", "green", "blue"]:
            for p in self.game_state.current_pieces[colour]:
                if position == p:
                    return colour
        return None
            
    
