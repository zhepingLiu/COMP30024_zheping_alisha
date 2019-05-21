"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

from best_AI_ever.game_board import GameBoard as GameBoard

class GameState:
    """
    GameState class that represents a single game state at a given time.
    Each GameState instance contains the current pieces for all teams on 
    the game board; the exit positions of all teams; the action that 
    applied to the predecessor state; the predecessor game state; number 
    of exits for all teams; and a GameBoard instance.
    """
    def __init__(self, current_pieces, exit_positions,
                 action, previous_state, number_of_exits):
        """
        Initialise a GameState instance

        Input: current_pieces: current pieces for all teams, dict type
               exit_positions: exit positions for all teams, dict type
               action: the action applied to the predecessor state, None at the
                       initial game state
               previous_state: the predecessor state
               number_of_exits: current number of exits for all teams, dict type
        """
        self.current_pieces = current_pieces
        self.exit_positions = exit_positions
        self.action = action
        self.previous_state = previous_state
        self.number_of_exits = number_of_exits
        self.game_board = GameBoard()

    def get_current_pieces(self):
        """
        Get current pieces for all players.
        Output: a dict, with colours of different players (teams) as keys,
                a frozenset contains the positions of the respective pieces for
                the player as values
        """
        return self.current_pieces

    def get_pieces(self, colour):
        """
        Get all pieces for a given player.
        Input: colour: the given player
        Output: a frozenset contains a list of pieces of the given player
        """
        return self.current_pieces[colour]

    def get_frozenset_pieces(self):
        """
        Get a frozenset of the all current pieces.
        Output: a frozenset of the current_pieces dict items.
        """
        return frozenset(self.current_pieces.items())

    def get_enemy_pieces(self, colour, is_list=False):
        """
        Get all enemy pieces respecting to a give player.
        Input: colour: the given player
               is_list: return a list of all enemy pieces if True, otherwise
               return a dict that contains pieces of different enemies in
               separate entries.
        
        Output: list of all enemy pieces, if is_list == True;
                dict with enemy colour as key, the frozenset of their respective
                pieces as value, if is_list == False
        """
        all_colours = ["red", "blue", "green"]
        # define the enemy colours for the given player colour
        enemy_colours = [x for x in all_colours if x != colour]

        if not is_list:
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
        """
        Get the pieces of the player before the given player.
        Input: colour: the given player
        Output: a frozenset contains the list of pieces of the previous player
        """
        if colour == "red":
            pre_player = "blue"
        elif colour == "green":
            pre_player = "red"
        else:
            pre_player = "green"

        return self.get_pieces(pre_player)

    def get_next_player_colour(self, colour):
        """
        Get the colour of the player after the given player.
        Input: colour: the given player
        Output: the colour of the next player
        """
        if colour == "blue":
            next_player = "red"
        elif colour == "red":
            next_player = "green"
        else:
            next_player = "blue"

        return next_player
    
    def get_next_player_pieces(self, colour):
        """
        Get the pieces of the player after the given player.
        Input: colour: the given player
        Output: a frozenset contains the list of pieces of the next player
        """
        if colour == "blue":
            next_player = "red"
        elif colour == "red":
            next_player = "green"
        else:
            next_player = "blue"
            
        return self.get_pieces(next_player)

    def get_colour(self, piece):
        """
        Get the colour of the given piece.
        Input: piece: the given piece
        Output: the colour of the player that owns this piece
        """
        for colour, pieces in self.current_pieces.items():
            if piece in pieces:
                return colour

        return
    
    def get_exit_positions(self):
        """
        Get exit positions for all players.
        Output: a dict with player colour as key, list of their respective
                exit positions as values
        """
        return self.exit_positions

    def get_action(self):
        """
        Get the action applied to predecessor.
        """
        return self.action

    def get_previous_state(self):
        """
        Get the predecessor state.
        """
        return self.previous_state

    def get_number_of_exits(self):
        """
        Get the number of exits for all players.
        Output: a dict with player colour as key, number of their respective
                exits as values
        """
        return self.number_of_exits

    def get_occupied_positions(self):
        """
        Get all hexes that are currently occupied, including pieces from all 
        teams including ourself.
        Output: a list contains all occupied positions
        """
        occupied_positions = []
        for _, pieces in self.current_pieces.items():
            occupied_positions += pieces

        return occupied_positions

    def is_sub_goal(self, piece, colour):
        """
        Check if the piece of the given player (colour) is at any exit 
        positions.
        Input: piece: the given piece
               colour: the given player
        Output: True, if the given piece is at an exit position;
                False, otherwise
        """
        if piece in self.exit_positions[colour]:
            return True
        
        return False

    def is_goal(self, colour):
        """
        Check if a given player is at goal state.
        """
        return self.number_of_exits[colour] >= 4

    def update(self, colour, action):
        """
        Update the game state according to the action applied by the given
        player.
        Input: colour: the given player
               action: the applied action
        """
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
        """
        Update the game state with a MOVE action applied by the given player.
        Input: colour: the given player
               action: the applied action
        """
        ACTION_POSITIONS = 1
        PRE_ACTION_POSITION = 0
        AFTER_ACTION_POSITION = 1

        # the position of the piece before applying the action
        pre_position = action[ACTION_POSITIONS][PRE_ACTION_POSITION]
        # the position of the piece after applying the action
        after_position = action[ACTION_POSITIONS][AFTER_ACTION_POSITION]

        new_pieces = list(self.current_pieces[colour])
        # apply the action by removing the previous position and add the 
        # after action position
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

    def is_protecting_pieces(self, colour):
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        protecting_pieces = []
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                potential_jump_median = self.game_board.get_jump_median(
                    enemy_piece, my_piece)
                if potential_jump_median != False and \
                        potential_jump_median in my_pieces:
                    protecting_pieces.append(my_piece)
                    break

        return protecting_pieces

    def get_protection_positions(self, colour):
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        protection_positions = []
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                jump = self.game_board.jump(enemy_piece, my_piece)
                if jump[0]:
                    protection_positions.append(jump[1])

        return protection_positions

    def get_risky_pieces(self, colour):
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        risky_pieces = []
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                jump = self.game_board.jump(enemy_piece, my_piece)
                if jump[0]:
                    risky_pieces.append(my_piece)

        return risky_pieces

    def same_colour(self, piece_1, piece_2):
        for _, pieces in self.current_pieces.items():
            if piece_1 in pieces and piece_2 in pieces:
                return True

        return False

    def construct_goal_actions(self):
        goal_actions = []
        game_state = self
        # game_state.print_game_state()

        while game_state.get_previous_state() != None:
            goal_actions.append(game_state.get_action())
            game_state = game_state.get_previous_state()
            # game_state.print_game_state()

        return list(reversed(goal_actions))

    def print_game_state(self, colour):
        print("My: %s; Enemies: %s; Action: %s; Exits: %s" % 
              (self.current_pieces[colour], 
               self.get_enemy_pieces(colour), 
               self.action, self.number_of_exits))

    def print_all_pre_states(self):
        current_state = self
        while current_state.previous_state != None:
            current_state.previous_state.print_game_state()
            current_state = current_state.previous_state
