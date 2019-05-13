from best_AI_ever.game_state import GameState as GameState
from best_AI_ever.game_board import GameBoard as GameBoard
from best_AI_ever.priority_queue import PriorityQueue as PriorityQueue

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.game_board = GameBoard()
        self.expanded_states = []

        start_positions = self.get_start_positions(colour)
        exit_positions = self.get_exit_positions()
        enemy_positions = self.get_enemy_positions(colour)
        number_of_exits = {"red": 0, "green": 0, "blue": 0}
        self.game_state = GameState(colour, start_positions, enemy_positions, 
                                    exit_positions, action=None, 
                                    previous_state=None, number_of_exits=
                                    number_of_exits)

    def action(self):
        # TODO: this will be the main function that make the player performs like AI
        return ("PASS", None)

    def update(self, colour, action):
        self.game_state.update(colour, action)
        return

    def a_star_search(self, game_state, colour):
        COST = 1
        heuristic = self.manhattan_heuristic
        # priority queue of states to be visited
        open_list = PriorityQueue()
        # list of expanded coordinates
        closed_list = []
        # dict of coordinates correspond to the cost from start to it
        g_score = {}
        # dict of coordinates correspond to the total cost to go to the goal
        # from start by passing through this coordinate
        f_score = {}

        # use the tuple of our teams pieces and the other teams' pieces as
        # the key to each different state 
        game_state_pieces = game_state.get_frozenset_pieces(colour)
        g_score[game_state_pieces] = 0
        f_score[game_state_pieces] = 0 + heuristic(game_state, colour)

        open_list.push(game_state, f_score[game_state_pieces])

        while not open_list.is_empty():
            current_state = open_list.pop()
            # current_state.print_game_state()
            # skip if the same combination of all pieces has already been 
            # visited before
            current_pieces = current_state.get_frozenset_pieces(colour)
            closed_list.append(current_pieces)

            # if the current state is the goal, return the actions to this state
            if current_state.is_goal(colour):
                return current_state.construct_goal_actions()

            for successor_state in self.generate_successor(current_state, 
                                                           colour):
                successor_pieces = successor_state.get_frozenset_pieces(colour)
                if successor_pieces in closed_list:
                    continue

                # the cost to get to current successor is the cost to get to
                # currentState + successor cost
                temp_g_score = g_score[current_pieces] + COST

                if successor_pieces not in g_score or \
                    g_score[successor_pieces] > temp_g_score:
                    temp_f_score = temp_g_score + heuristic(successor_state, 
                                                            colour)
                    open_list.push(successor_state, temp_f_score)
                    g_score[successor_pieces] = temp_g_score

        # return [] list of actions when no solution can be found
        print("No solution found")
        return []

    def generate_successor(self, game_state, colour):
        exit_successors = self.generate_exit_successor(game_state, colour)
        jump_successors = self.generate_jump_successor(game_state, colour)
        move_successors = self.generate_move_successor(game_state, colour)

        successor = exit_successors + jump_successors + move_successors

        return successor

    def generate_exit_successor(self, game_state, colour):
        exit_successors = []
        current_pieces = game_state.get_pieces(colour)

        for piece in current_pieces:
            if game_state.is_sub_goal(piece, colour):
                new_pieces = [x for x in current_pieces if x != piece]
                action = self.get_action("EXIT", piece, None)
                new_game_state = self.generate_new_game_state(game_state, 
                                                            new_pieces, action)
                exit_successors.append(new_game_state)
        
        return exit_successors

    def generate_jump_successor(self, game_state, colour):
        jump_successors = []
        current_pieces = game_state.get_pieces(colour)
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
                        new_pieces.append(jump_destination)
                        new_game_state = self.generate_new_game_state(
                                                game_state, new_pieces, action)
                        jump_successors.append(new_game_state)

        return jump_successors

    def generate_move_successor(self, game_state, colour):
        move_successors = []
        current_pieces = game_state.get_pieces(colour)
        occupied_positions = game_state.get_occupied_positions()
        game_board = self.game_board.get_game_board()

        for position in game_board:
            for piece in current_pieces:
                if position not in occupied_positions and \
                    self.game_board.next_to(piece, position):
                     # generate all successor states by applying action MOVE
                     action = self.get_action("MOVE", piece, position)
                     new_pieces = [x for x in current_pieces if x != piece]
                     new_pieces.append(position)
                     new_game_state = self.generate_new_game_state(
                         game_state, new_pieces, action)
                     move_successors.append(new_game_state)

        return move_successors
                
    def generate_new_game_state(self, pre_game_state, new_pieces, action):
        colour = pre_game_state.get_colour()
        enemy_pieces = pre_game_state.get_enemy_pieces(colour)
        exit_positions = pre_game_state.get_exit_positions()
        number_of_exits = dict(pre_game_state.get_number_of_exits())

        # TODO: Temporary handle
        if action[0] == "EXIT":
            number_of_exits[colour] += 1

        return GameState(colour, new_pieces, enemy_pieces, exit_positions, 
                            action, pre_game_state, number_of_exits)

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
            start_positions = [(-3, 0), (-3, 1), (-3, 2), (-3, 3)]
        elif colour == "green":
            start_positions = [(0, -3), (1, -3), (2, -3), (-3, -3)]
        else:
            start_positions = [(3, 0), (2, 1), (1, 2), (0, 3)]

        return start_positions

    def get_exit_positions(self):
        exit_positions = {}

        exit_positions["red"] = [(3, -3), (3, -2), (3, -1), (3, 0)]
        exit_positions["green"] = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
        exit_positions["blue"] = [(-3, 0), (-2, -1), (-1, -2), (0, -3)]

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
        # for enemy_colour in enemy_colours:
        #     enemy_positions[enemy_colour] = \
        #         self.get_start_positions(enemy_colour)

        return enemy_positions

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

        # take the minimum distance (to make sure the heuristic is admissible) from
        # distances to all goals
        for i in range(1, 4):
            temp_dist = (abs(position[0] - goal[i][0]) + abs(position[0]
                                                            + position[1] - goal[i][0] - goal[i][1]) +
                        abs(position[1] - goal[i][1])) / 2
            if temp_dist < dist0:
                dist0 = temp_dist

        return int(dist0)

    # compute the sum of the distances from all pieces to their closest goals
    # Input: current_state: the current state of the game
    # Output: the sum of the distances from all pieces to their closest goals
    def manhattan_heuristic(self, current_state, colour):
        # current_state["position"] is frozenset, convert it back to a list
        positions = current_state.get_pieces(colour)

        heuristic = 0
        for position in positions:
            # assuming all moves are jump (move distance = 2), + 1 exit action
            heuristic += (self.manhattan_distance(position, colour) / 2 + 1)

        return heuristic
