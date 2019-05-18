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

    def get_my_pieces(self):
        return self.current_pieces[self.colour]

    def get_enemy_pieces(self, colour, list=False):
        all_colours = ["red", "blue", "green"]
        enemy_colours = [x for x in all_colours if x != colour]

        if not list:
            # return enemy pieces as dict, keys are the enemy colours
            enemy_pieces = {}
            for enemy_colour in enemy_colours:
                enemy_pieces[enemy_colour] = self.current_pieces[enemy_colour]            
        else:
            # return all enemy pieces as one list
            enemy_pieces = []
            for enemy_colour in enemy_colours:
                enemy_pieces += self.current_pieces[enemy_colour]

        return enemy_pieces

    def get_pre_player_pieces(self, colour):
        if self.colour == "red":
            pre_player = "blue"
        elif self.colour == "green":
            pre_player = "red"
        else:
            pre_player = "green"

        return self.get_pieces(pre_player)

    def get_next_player_colour(self, colour):
        if self.colour == "blue":
            next_player = "red"
        elif self.colour == "red":
            next_player = "green"
        else:
            next_player = "blue"

        return next_player
    
    def get_next_player_pieces(self, colour):
        if self.colour == "blue":
            next_player = "red"
        elif self.colour == "red":
            next_player = "green"
        else:
            next_player = "blue"
            
        return self.get_pieces(next_player)
    
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

        new_pieces = list(self.current_pieces[colour])
        new_pieces.remove(pre_position)
        new_pieces.append(after_position)

        self.current_pieces[colour] = frozenset(new_pieces)

        return

    def update_jumping(self, colour, action):
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0
        AFTER_ACTION_POSITION = 1

        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]
        after_position = action[ACTION_POSITIONS][AFTER_ACTION_POSITION]

        new_pieces = list(self.current_pieces[colour])
        new_pieces.remove(pre_position)
        new_pieces.append(after_position)
        self.current_pieces[colour] = frozenset(new_pieces)
        self.turn_piece(pre_position, after_position, colour)

        return

    def update_exiting(self, colour, action):
        ACTION_POSITIONS = 1

        pre_position = action[ACTION_POSITIONS]

        new_pieces = list(self.current_pieces[colour])
        new_pieces.remove(pre_position)
        self.current_pieces[colour] = frozenset(new_pieces)

        self.number_of_exits[colour] += 1

        return

    def turn_piece(self, pre_position, after_position, colour):
        taken_piece = self.game_board.get_jump_median(
                                        pre_position, after_position)

        for taken_colour, pieces in self.current_pieces.items():
            # if the colour of the taken piece is different from the colour
            # of the piece took it
            if taken_colour != colour and taken_piece in pieces:
                taken_colour_pieces = list(self.current_pieces[taken_colour])
                taken_colour_pieces.remove(taken_piece)
                self.current_pieces[taken_colour] = frozenset(
                                                    taken_colour_pieces)

                new_pieces = list(self.current_pieces[colour])
                new_pieces.append(taken_piece)
                self.current_pieces[colour] = frozenset(new_pieces)

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
