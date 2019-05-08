class GameState:
    def __init__(self, colour, current_pieces, enemy_pieces, exit_positions):
        self.colour = colour
        self.current_pieces = current_pieces
        self.enemy_pieces = enemy_pieces
        self.exit_positions = exit_positions
        self.number_of_exits = 0

    def get_current_pieces(self):
        return self.current_pieces

    def get_enemy_pieces(self):
        return self.enemy_pieces

    def get_exit_positions(self):
        return self.exit_positions

    def is_sub_goal(self):
        for piece in self.current_pieces:
            if piece in self.exit_positions:
                return True
        
        return False

    def is_goal(self):
        return self.number_of_exits == 4

    def update(self, colour, action):
        # TODO: update the game_state according to the previous action
        # actions example: ("MOVE", ((0, 0), (0, 1)))
        #                  ("JUMP", ((0, 1), (-2, 3)))
        #                  ("EXIT", (-2, 3))
        #                  ("PASS", None)
        ACTION_NAME = 0

        if action[ACTION_NAME] == "MOVE" or action[ACTION_NAME] == "JUMP":
            self.update_piece_movement(colour, action)
        elif action[ACTION_NAME] == "EXIT":
            self.update_exiting(colour, action)
        
        # do nothing if the action is "PASS"
        return

    def update_piece_movement(self, colour, action):
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0
        AFTER_ACTION_POSITION = 1

        if colour == self.colour:
            self.current_pieces.remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])
            self.current_pieces.append(
                action[ACTION_POSITIONS][AFTER_ACTION_POSITION])
        else:
            self.enemy_pieces[colour].remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])
            self.enemy_pieces[colour].append(
                action[ACTION_POSITIONS][AFTER_ACTION_POSITION])

        return

    def update_exiting(self, colour, action):
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0

        if colour == self.colour:
            self.current_pieces.remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])
        else:
            self.enemy_pieces[colour].remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])

        return