class GameBoard:
    def __init__(self):
        self.game_board = self.get_game_board()

    """
    Get all valid coordinates on the game board
    """
    def get_game_board(self):
        if self.game_board == None:
            ran = range(-3, 4)
            self.game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

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
           position_2: the coordinate of the given block
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
