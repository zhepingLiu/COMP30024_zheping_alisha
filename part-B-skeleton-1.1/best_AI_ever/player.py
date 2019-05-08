from best_AI_ever.game_state import GameState as GameState

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.game_board = self.get_game_board()
        self.expanded_states = []

        start_positions = self.get_start_positions(colour)
        exit_positions = self.get_exit_positions(colour)
        enemy_positions = self.get_enemy_positions(colour)
        
        self.current_game_state = GameState(colour, start_positions, 
                                    enemy_positions, exit_positions)

    def action(self):
        # TODO: this will be the main function that make the player performs like AI
        return ("PASS", None)

    def update(self, colour, action):
        self.current_game_state.update(colour, action)
        return

    def generate_successor(self, game_state):
        # TODO: similar to the generate_successor function in part A
        successor = []
        current_position = game_state.get_current_pieces()

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

    def get_game_board(self):
        ran = range(-3, 4)
        game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

        return game_board