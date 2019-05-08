from best_AI_ever.game_state import GameState as GameState
from best_AI_ever.game_board import GameBoard as GameBoard

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.game_board = GameBoard()
        self.expanded_states = []

        start_positions = self.get_start_positions(colour)
        exit_positions = self.get_exit_positions(colour)
        enemy_positions = self.get_enemy_positions(colour)
        
        self.game_state = GameState(colour, start_positions, enemy_positions, 
                                    None, exit_positions, [], 0)

    def action(self):
        # TODO: this will be the main function that make the player performs like AI
        return ("PASS", None)

    def update(self, colour, action):
        self.game_state.update(colour, action)
        return

    def generate_successor(self, game_state):
        # TODO: similar to the generate_successor function in part A
        exit_successors = self.generate_exit_successor(game_state)
        jump_successors = self.generate_jump_successor(game_state)
        move_successors = self.generate_move_successor(game_state)

        successor = exit_successors + jump_successors + move_successors

        return successor

    def generate_exit_successor(self, game_state):
        exit_successors = []
        current_pieces = game_state.get_current_pieces()

        for piece in current_pieces:
            if game_state.is_sub_goal(piece):
                new_pieces = [x for x in current_pieces if x != piece]
                action = self.get_action("EXIT", piece, None)
                new_game_state = self.generate_new_game_state(game_state, 
                                                            new_pieces, action)
                exit_successors.append(new_game_state)
        
        return exit_successors

    def generate_jump_successor(self, game_state):
        jump_successors = []
        current_pieces = game_state.get_current_pieces()
        occupied_positions = game_state.get_occupied_positions()

        for position in occupied_positions:
            for piece in current_pieces:
                # position: the potential jump medium (NOT jump destination)
                # piece: the potential start position
                # jump medium should be next to the piece
                if self.game_board.next_to(position, piece):
                    # generate the successor coordinate by applying action JUMP
                    jump_destination = self.game_board.jump(piece, position)
                    # if there is a possible JUMP coordinate and this coordinate
                    # is not occupied by other pieces
                    if jump_destination[0] and \
                        jump_destination[1] not in occupied_positions:
                        # assign the coordinate to the variable jump_destination
                        jump_destination = jump_destination[1]
                        action = self.get_action("JUMP", 
                                                    piece, jump_destination)
                        # TODO: by applying jump over other team's pieces, that
                        # enemy piece will turn to our colour
                        new_pieces = [x for x in current_pieces if x != piece]
                        new_game_state = self.generate_new_game_state(
                                                game_state, new_pieces, action)
                        jump_successors.append(new_game_state)

        return jump_successors

    def generate_move_successor(self, game_state):
        move_successors = []
        current_pieces = game_state.get_current_pieces()
        occupied_positions = game_state.get_occupied_positions()
        game_board = self.game_board.get_game_board()

        for position in game_board:
            for piece in current_pieces:
                if position not in occupied_positions and \
                    self.game_board.next_to(piece, position):
                     # generate all successor states by applying action MOVE
                     action = self.get_action("MOVE", piece, position)
                     new_pieces = [x for x in current_pieces if x != piece]
                     new_game_state = self.generate_new_game_state(
                         game_state, new_pieces, action)
                     move_successors.append(new_game_state)

        return move_successors
                
    def generate_new_game_state(self, pre_game_state, new_pieces, action):
        colour = pre_game_state.get_colour()
        enemy_pieces = pre_game_state.get_enemy_pieces()
        exit_positions = pre_game_state.get_exit_positions()
        expanded_states = pre_game_state.get_expanded_states()
        expanded_states.append(pre_game_state)
        number_of_exits = pre_game_state.get_number_of_exits()

        return GameState(colour, new_pieces, enemy_pieces, exit_positions, 
                            action, expanded_states, number_of_exits)

    def get_action(self, action_name, start_position, destination):
        if action_name == "MOVE" or action_name == "JUMP":
            return (action_name, (start_position, destination))
        elif action_name == "EXIT":
            return (action_name, start_position)
        else:
            # "PASS" action
            return (action_name, None)

    def get_start_positions(self, colour):
        # TODO: if red, start pieces = [...], etc.
        start_positions = []

        if colour == "red":
            start_positions = []
        elif colour == "green":
            start_positions = []
        else:
            start_positions = []

        return start_positions

    def get_exit_positions(self, colour):
        exit_positions = []
        if colour == "red":
            exit_positions = [(3, -3), (3, -2), (3, -1), (3, 0)]
        elif colour == "green":
            exit_positions = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
        elif colour == "blue":
            exit_positions = [(-3, 0), (-2, -1), (-1, -2), (0, -3)]

        return exit_positions

    def get_enemy_positions(self, colour):
        enemy_colours = []

        if colour == "red":
            enemy_colours = ["green", "blue"]
        elif colour == "green":
            enemy_colours = ["red", "blue"]
        elif colour == "blue":
            enemy_colours = ["red", "green"]

        enemy_positions = {}
        for enemy_colour in enemy_colours:
            enemy_positions[enemy_colour] = \
                self.get_start_positions(enemy_colour)

        return enemy_positions
