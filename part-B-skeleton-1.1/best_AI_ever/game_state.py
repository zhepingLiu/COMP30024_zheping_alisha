"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

from best_AI_ever.game_board import GameBoard as GameBoard
import copy

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
        Initialise a GameState instance.

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

        previous_state = copy.deepcopy(self)

        if action[ACTION_NAME] == "MOVE":
            self.update_moving(colour, action)
        elif action[ACTION_NAME] == "JUMP":
            self.update_jumping(colour, action)
        elif action[ACTION_NAME] == "EXIT":
            self.update_exiting(colour, action)
        else:
            # PASS action
            self.action = action
        
        self.previous_state = previous_state
        
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
        self.action = action

        return

    def update_jumping(self, colour, action):
        """
        Update the game state with a JUMP action applied by the given player.
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
        # turn the colour of the captured piece if there is any
        self.turn_piece(pre_position, after_position, colour)

        self.action = action

        return

    def update_exiting(self, colour, action):
        """
        Update the game state with a EXIT action applied by the given player.
        Input: colour: the given player
               action: the applied action
        """
        ACTION_POSITIONS = 1

        # the position of the piece before applying the action
        # for EXIT action, there is no after-action position
        pre_position = action[ACTION_POSITIONS]

        # apply the action by removing the previous position and increment
        # the number of exits
        new_pieces = list(self.current_pieces[colour])
        new_pieces.remove(pre_position)
        self.current_pieces[colour] = frozenset(new_pieces)
        self.number_of_exits[colour] += 1

        self.action = action

        return

    def turn_piece(self, pre_position, after_position, colour):
        """
        Check if there is any piece captured by applying JUMP action,
        if there is any, turn the colour of the captured piece.
        Input: pre_position: the previous position before applying JUMP
               after_position: the after position after applying JUMP
               colour: the colour of the player applied JUMP action
        """
        # compute the position of the jump median
        taken_piece = self.game_board.get_jump_median(
                                        pre_position, after_position)

        # check if the piece at jump median belongs to other players
        for taken_colour, pieces in self.current_pieces.items():
            # if the colour of the taken piece is different from the colour
            # of the piece took it
            if taken_colour != colour and taken_piece in pieces:
                taken_colour_pieces = list(self.current_pieces[taken_colour])
                taken_colour_pieces.remove(taken_piece)
                self.current_pieces[taken_colour] = frozenset(
                                                    taken_colour_pieces)
                # remove the taken piece from its original player and add
                # it to the player who applied JUMP action
                new_pieces = list(self.current_pieces[colour])
                new_pieces.append(taken_piece)
                self.current_pieces[colour] = frozenset(new_pieces)

        return

    def is_protecting_pieces(self, colour):
        """
        Get the pieces that are protecting other pieces (blocking enemies'
        pieces to apply JUMP action to capture one of the player's piece).
        Input: colour: the given player
        Output: a list contains all pieces that are protecting other pieces for
                the given player
        """
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        protecting_pieces = []
        # iterate through all my pieces and enemy pieces
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                # compute the jump median (if any)
                potential_jump_median = self.game_board.get_jump_median(
                    enemy_piece, my_piece)
                # if there is a piece at jump median and it belongs to us,
                # add my_piece to the protecting_pieces list
                if potential_jump_median != False and \
                        potential_jump_median in my_pieces:
                    protecting_pieces.append(my_piece)
                    break

        return protecting_pieces

    def get_protection_positions(self, colour):
        """
        Get the positions that can result protection for other pieces for the
        given player.
        Input: colour: the given player
        """
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        protection_positions = []
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                # if an enemy is available to JUMP over one of our piece,
                # add the destination of that JUMP action to the list
                jump = self.game_board.jump(enemy_piece, my_piece)
                if jump[0]:
                    protection_positions.append(jump[1])

        return protection_positions

    def get_risky_pieces(self, colour):
        """
        Get the pieces that could be captured by the enemies for the 
        given player.
        Input: colour: the given player
        """
        my_pieces = self.get_pieces(colour)
        enemy_pieces = self.get_enemy_pieces(colour, True)
        risky_pieces = []
        for my_piece in my_pieces:
            for enemy_piece in enemy_pieces:
                # if an enemy is available to JUMP over one of our piece,
                # add my piece to the risky_pieces list
                jump = self.game_board.jump(enemy_piece, my_piece)
                if jump[0]:
                    risky_pieces.append(my_piece)

        return risky_pieces

    def same_colour(self, piece_1, piece_2):
        """
        Check if two pieces belongs to the same player (same colour)/
        Input: piece_1: the first given piece
               piece_2: the second given piece
        """
        for _, pieces in self.current_pieces.items():
            if piece_1 in pieces and piece_2 in pieces:
                return True

        return False

    def construct_goal_actions(self):
        """
        Construct the sequence of actions from the initial state to the
        current state.
        Output: list of actions from initial state to current state
        """
        goal_actions = []
        game_state = self

        # loop until the game_state is None, i.e. initial state has been reached
        while game_state.get_previous_state() != None:
            goal_actions.append(game_state.get_action())
            game_state = game_state.get_previous_state()

        return list(reversed(goal_actions))