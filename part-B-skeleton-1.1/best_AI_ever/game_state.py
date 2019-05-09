class GameState:
    def __init__(self, colour, current_pieces, enemy_pieces, exit_positions,
                 action, expanded_states, number_of_exits):
        self.colour = colour
        self.current_pieces = current_pieces
        self.enemy_pieces = enemy_pieces
        self.exit_positions = exit_positions
        self.action = action
        self.expanded_states = expanded_states
        self.number_of_exits = number_of_exits

    def get_colour(self):
        return self.colour

    def get_current_pieces(self):
        return self.current_pieces

    def get_enemy_pieces(self):
        return self.enemy_pieces

    def get_exit_positions(self):
        return self.exit_positions

    def get_expanded_states(self):
        return self.expanded_states

    def get_number_of_exits(self):
        return self.number_of_exits

    def get_occupied_positions(self):
        # return all hexes that are currently occupied,
        # including pieces from all teams including ourself
        occupied_positions = self.current_pieces
        for _, pieces in self.enemy_pieces.items():
            occupied_positions += pieces

        return occupied_positions

    def is_sub_goal(self, piece):
        if piece in self.exit_positions:
            return True
        
        return False

    def is_goal(self):
        return self.number_of_exits == 4

    def update(self, colour, action):
        # update the game_state according to the previous action
        # actions example: ("MOVE", ((0, 0), (0, 1)))
        #                  ("JUMP", ((0, 1), (-2, 3)))
        #                  ("EXIT", (-2, 3))
        #                  ("PASS", None)
        ACTION_NAME = 0

        if action[ACTION_NAME] == "MOVE":
            self.update_moving(colour, action)
        elif action[ACTION_NAME] == "JUMP":
            self.update_jumping(colour, action)
        elif action[ACTION_NAME] == "EXIT":
            self.update_exiting(colour, action)
        
        # do nothing if the action is "PASS"
        return

    def update_moving(self, colour, action):
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

    def update_jumping(self, colour, action):
        # TODO: by applying action JUMP, the jump medium will turn to
        # the colour of who ever did the JUMP action
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0
        AFTER_ACTION_POSITION = 1

        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]
        after_position = action[ACTION_POSITIONS][AFTER_ACTION_POSITION]

        if colour == self.colour:
            self.current_pieces.remove(pre_position)
            self.current_pieces.append(after_position)
            # acquire the enemy piece if possible
            # TODO: first step, we need to calculate the coordinate of the piece being acquired
        else:
            self.enemy_pieces[colour].remove(pre_position)
            self.enemy_pieces[colour].append(after_position)
            # TODO: update if any other piece is taken by the enemy

        self.turn_piece(pre_position, after_position, colour)
        return

    def update_exiting(self, colour, action):
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0

        if colour == self.colour:
            self.current_pieces.remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])
            self.number_of_exits += 1
        else:
            self.enemy_pieces[colour].remove(
                action[ACTION_POSITIONS][PRE_ACTION_POSITION])

        return

    def turn_piece(self, pre_position, after_position, colour):
        taken_piece = self.get_jump_medium(pre_position, after_position)
        # if the colour of the taken piece and the colour of the piece at after_position
        # are not the same, change the colour of the taken piece to the colour of the piece at after_position
        if colour == self.colour:
            for taken_colour, enemy_pieces in self.enemy_pieces.items():
                for piece in enemy_pieces:
                    if piece == taken_piece:
                        self.enemy_pieces[taken_colour].remove(taken_piece)
                        self.current_pieces.append(taken_piece)
                        return
        else:
            # check pieces of ours and pieces of another enemy
            for piece in self.current_pieces:
                if piece == taken_piece:
                    self.current_pieces.remove(taken_piece)
                    self.enemy_pieces[colour].append(taken_piece)
                    return

            for taken_colour, enemy_pieces in self.enemy_pieces.items():
                if taken_colour == colour:
                    continue
                for piece in enemy_pieces:
                    if piece == taken_piece:
                        self.enemy_pieces[taken_colour].remove(taken_piece)
                        self.enemy_pieces[colour].append(taken_piece)
                        return
        return


    def get_jump_medium(self, position_1, position_2):
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
        
        return (q, r)
