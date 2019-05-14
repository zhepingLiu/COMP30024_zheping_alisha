from best_AI_ever.game_board import GameBoard as GameBoard

class GameState:
    def __init__(self, colour, current_pieces, exit_positions,
                 action, previous_state, number_of_exits):
        self.colour = colour
        self.current_pieces = current_pieces
        self.exit_positions = exit_positions
        self.action = action
        self.previous_state = previous_state
        self.number_of_exits = number_of_exits
        self.game_board = GameBoard()

    def get_colour(self):
        return self.colour

    def get_current_pieces(self):
        return self.current_pieces

    def get_pieces(self, colour):
        return self.current_pieces[colour]

    def get_frozenset_pieces(self):
        return frozenset(self.current_pieces.items())

    def get_enemy_pieces(self, colour):
        all_colours = ["red", "blue", "green"]
        enemy_colours = [x for x in all_colours if x != colour]

        enemy_pieces = {}
        for enemy_colour in enemy_colours:
            enemy_pieces[enemy_colour] = self.current_pieces[enemy_colour]
        
        return enemy_pieces

    def get_exit_positions(self):
        return self.exit_positions

    def get_action(self):
        return self.action

    def get_previous_state(self):
        return self.previous_state

    def get_number_of_exits(self):
        return self.number_of_exits

    def get_occupied_positions(self):
        # return all hexes that are currently occupied,
        # including pieces from all teams including ourself
        occupied_positions = []
        for _, pieces in self.current_pieces.items():
            occupied_positions += pieces

        return occupied_positions

    def is_sub_goal(self, piece, colour):
        if piece in self.exit_positions[colour]:
            return True
        
        return False

    def is_goal(self, colour):
        return self.number_of_exits[colour] == 4

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

        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]
        after_position = action[ACTION_POSITIONS][AFTER_ACTION_POSITION]

        self.current_pieces[colour].remove(pre_position)
        self.current_pieces[colour].append(after_position)

        return

    def update_jumping(self, colour, action):
        # TODO: by applying action JUMP, the jump medium will turn to
        # the colour of who ever did the JUMP action
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0
        AFTER_ACTION_POSITION = 1

        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]
        after_position = action[ACTION_POSITIONS][AFTER_ACTION_POSITION]

        self.current_pieces[colour].remove(pre_position)
        self.current_pieces[colour].append(after_position)
        self.turn_piece(pre_position, after_position, colour)

        return

    def update_exiting(self, colour, action):
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0

        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]

        self.current_pieces[colour].remove(pre_position)
        self.number_of_exits[colour] += 1

        return

    def turn_piece(self, pre_position, after_position, colour):
        taken_piece = self.game_board.get_jump_medium(
                                        pre_position, after_position)

        for taken_colour, pieces in self.current_pieces.items():
            # if the colour of the taken piece is different from the colour
            # of the piece took it
            if taken_colour != colour and taken_piece in pieces:
                self.current_pieces[taken_colour].remove(taken_piece)
                self.current_pieces[colour].append(taken_piece)

        return

    def construct_goal_actions(self):
        goal_actions = []
        game_state = self
        # game_state.print_game_state()

        while game_state.get_previous_state() != None:
            goal_actions.append(game_state.get_action())
            game_state = game_state.get_previous_state()
            # game_state.print_game_state()

        return list(reversed(goal_actions))

    def print_game_state(self):
        print("My: %s; Enemies: %s; Action: %s; Exits: %s" % 
              (self.current_pieces[self.colour], 
               self.get_enemy_pieces(self.colour), 
               self.action, self.number_of_exits))

    def print_all_pre_states(self):
        current_state = self
        while current_state.previous_state != None:
            current_state.previous_state.print_game_state()
            current_state = current_state.previous_state
