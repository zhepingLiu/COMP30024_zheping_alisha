from best_AI_ever.game_state import GameState as GameState
from best_AI_ever.game_board import GameBoard as GameBoard
from best_AI_ever.priority_queue import PriorityQueue as PriorityQueue
import copy

class Player:
    def __init__(self, colour):
        self.colour = colour
        self.game_board = GameBoard()
        self.expanded_states = []

        start_positions = self.get_start_positions()
        exit_positions = self.get_exit_positions()
        # enemy_positions = self.get_enemy_positions(colour)
        number_of_exits = {"red": 0, "green": 0, "blue": 0}
        self.game_state = GameState(colour, start_positions, 
                                    exit_positions, action=None, 
                                    previous_state=None, number_of_exits=
                                    number_of_exits)

    def action(self):
        # TODO: this will be the main function that make the player performs
        # like an AI
        LIMIT = 6
        my_desirable_successors = self.get_desirable_successors(self.colour)

        if my_desirable_successors == []:
            available_successors = self.generate_successor(self.game_state, 
                                                           self.colour)
            if available_successors == []:
                return ("PASS", None)
            my_desirable_successors = available_successors

        next_player = self.game_state.get_next_player_colour(self.colour)
        current_successors = my_desirable_successors[:]
        i = 0
        while i < LIMIT:
            next_player_successors = []
            for successor in current_successors:
                next_player_successors.append(self.choose_optimal_successor(
                                                successor, next_player))
                next_player = self.game_state.get_next_player_colour(
                                                next_player)
                current_successors = next_player_successors
            i += 1

        # next_player = self.game_state.get_next_player_colour(self.colour)
        # enemy_1_successors = []
        # for successor in my_desirable_successors:
        #     enemy_1_successors.append(self.choose_optimal_successor(
        #                                     successor, next_player))
        
        # next_player = self.game_state.get_next_player_colour(next_player)
        # enemy_2_successors = []
        # for successor in enemy_1_successors:
        #     enemy_2_successors.append(self.choose_optimal_successor(
        #                                     successor, next_player))

        max_reward = 0
        max_reward_index = -1
        for i in range(len(next_player_successors)):
            successor = next_player_successors[i]
            rewards = self.get_state_reward(successor)
            if rewards[self.colour] > max_reward:
                max_reward = rewards[self.colour]
                max_reward_index = i

        try:
            action = my_desirable_successors[max_reward_index].get_action()
        except:
            print(len(my_desirable_successors))
            print(len(next_player_successors))
            print(max_reward_index)

        return action

    def update(self, colour, action):
        self.game_state.update(colour, action)
        return

    def choose_optimal_successor(self, game_state, colour):
        INFINITE = 99999
        SENTINEL = -1
        # TODO: basic idea: remove all actions that does not look good (gives us
        # negative rewards), then choose the action gives the smallest h value
        # among all available actions
        # Player order: Red -> Green -> Blue

        available_successors = self.generate_successor(game_state, self.colour)

        # return Pass when no actions available
        if available_successors == []:
            return self.generate_new_game_state(game_state, 
                        game_state.get_current_pieces(), ("PASS", None))

        desirable_successors = self.get_desirable_successors(self.colour)

        jump_capturing_pieces = set()
        distances = self.game_board.distance_to_enemy_pieces(game_state)
        # distances: a dict of dict, first key is our pieces, second key is
        # enemy pieces, the value is the distance between them
        for my_piece, enemy_distances in distances.items():
            for enemy_piece, enemy_distance in enemy_distances.items():
                # TODO: we can find those pieces that are capable to 
                # capture enemies' pieces
                if enemy_distance == 1:
                    jump_capturing_pieces.add(my_piece)
        
        # when all actions are not desirable, but we have to return one of them
        if desirable_successors == []:
            h_min = INFINITE
            h_min_index = SENTINEL
            for i in range(len(available_successors)):
                h_successor = self.manhattan_heuristic(available_successors[i],
                                                        colour)
                if h_successor < h_min:
                    h_min = h_successor
                    h_min_index = i
            
            return available_successors[h_min_index]

        final_desirable_successors = []
        for i in range(len(desirable_successors)):
            if desirable_successors[i].get_action() == "JUMP" and \
                len(desirable_successors[i].get_my_pieces()) > \
                len(game_state.get_my_pieces()):
                final_desirable_successors.append(desirable_successors[i])

        if final_desirable_successors == []:
            final_desirable_successors = desirable_successors

        # choose the action that brings the smallest h value in its successor
        r_max = 0
        r_max_index = SENTINEL
        for i in range(len(final_desirable_successors)):
            r_successor = self.get_state_reward(final_desirable_successors[i])
            if r_successor[colour] > r_max:
                r_max = r_successor[colour]
                r_max_index = i

        return final_desirable_successors[r_max_index]
    
    def get_desirable_successors(self, colour):
        available_successors = self.generate_successor(
                                    self.game_state, colour)
        available_actions = [x.get_action() for x in available_successors]

        # Stop moving the piece when there is enemy piece in two hexes from it,
        # if enemy piece is one hex away (next to us), jump over it or move
        # apart from it (move to the direction that increase the distance);
        # detailed strategy based on the heuristic (the distance to the goal),
        # if jump can take us forward to the goal, then jump; otherwise move
        # apart from it
        desirable_actions = available_actions
        desirable_successors = available_successors
        for successor, successor_action in zip(available_successors,
                                               available_actions):
            if successor_action[0] == 'EXIT':
                continue

            after_position = successor_action[1][1]
            # we use the enemy pieces get from successor state, if some pieces
            # are captured by us, it will not be an enemy piece in that state
            for enemy in successor.get_enemy_pieces(self.colour, True):
                # if the distance after applying the successor action is below
                # 2, i.e. distance = 1 since 0 is impossible, remove this action
                if (self.game_board.hex_distance(after_position, enemy) < 2 and
                    not self.game_board.no_jump_for_enemy(
                        successor, after_position, enemy)):
                    # print("Should be removed: (%s, %s)" % (successor_action))
                    desirable_actions = [x for x in desirable_actions
                                         if x != successor_action]
                    desirable_successors = [x for x in desirable_successors
                                            if x != successor]

        return desirable_successors

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
        game_state_pieces = game_state.get_my_pieces()
        g_score[game_state_pieces] = 0
        f_score[game_state_pieces] = 0 + heuristic(game_state, colour)

        open_list.push(game_state, f_score[game_state_pieces])

        while not open_list.is_empty():
            current_state = open_list.pop()
            # TODO: testing purpose
            # skip if the same combination of all pieces has already been 
            # visited before
            current_pieces = current_state.get_my_pieces()
            closed_list.append(current_pieces)

            # if the current state is the goal, return the actions to this state
            if current_state.is_goal(colour):
                return current_state.construct_goal_actions()

            for successor_state in self.generate_successor(current_state, 
                                                           colour):
                successor_pieces = successor_state.get_my_pieces()
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

        successors = exit_successors + jump_successors + move_successors

        return list(set(successors))

    def generate_exit_successor(self, game_state, colour):
        exit_successors = []
        current_pieces = game_state.get_current_pieces()

        for piece in current_pieces[colour]:
            if game_state.is_sub_goal(piece, colour):
                new_pieces = copy.deepcopy(current_pieces)
                new_pieces[colour] = frozenset([x for x in 
                                    current_pieces[colour] if x != piece])
                action = self.get_action("EXIT", piece, None)
                new_game_state = self.generate_new_game_state(game_state, 
                                                            new_pieces, action)
                exit_successors.append(new_game_state)

        return exit_successors

    def generate_jump_successor(self, game_state, colour):
        jump_successors = []
        current_pieces = game_state.get_current_pieces()
        occupied_positions = game_state.get_occupied_positions()

        for position in occupied_positions:
            for piece in current_pieces[colour]:
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
                        new_pieces = copy.deepcopy(current_pieces)
                        new_pieces[colour] = [x for x in current_pieces[colour] 
                                              if x != piece]
                        new_pieces[colour].append(jump_destination)
                        new_pieces[colour] = frozenset(new_pieces[colour])
                        new_game_state = self.generate_new_game_state(
                                                game_state, new_pieces, action)
                        # by applying jump over other team's pieces, that
                        # enemy piece will turn to our colour
                        new_game_state.turn_piece(piece, 
                                                  jump_destination, colour)
                        jump_successors.append(new_game_state)

        return jump_successors

    def generate_move_successor(self, game_state, colour):
        move_successors = []
        current_pieces = game_state.get_current_pieces()
        occupied_positions = game_state.get_occupied_positions()
        game_board = self.game_board.get_game_board()

        for position in game_board:
            for piece in current_pieces[colour]:
                if position not in occupied_positions and \
                    self.game_board.next_to(piece, position):
                    # generate all successor states by applying action MOVE
                    action = self.get_action("MOVE", piece, position)
                    new_pieces = copy.deepcopy(current_pieces)
                    new_pieces[colour] = [x for x in current_pieces[colour]
                                          if x != piece]
                    new_pieces[colour].append(position)
                    new_pieces[colour] = frozenset(new_pieces[colour])
                    new_game_state = self.generate_new_game_state(
                        game_state, new_pieces, action)
                    move_successors.append(new_game_state)

        return move_successors
                
    def generate_new_game_state(self, pre_game_state, new_pieces, action):
        colour = pre_game_state.get_colour()
        # enemy_pieces = pre_game_state.get_enemy_pieces(colour)
        exit_positions = pre_game_state.get_exit_positions()
        number_of_exits = pre_game_state.get_number_of_exits().copy()

        if action[0] == "EXIT":
            number_of_exits[colour] += 1

        return GameState(colour, new_pieces, exit_positions, 
                            action, pre_game_state, number_of_exits)

    def get_action(self, action_name, start_position, destination):
        if action_name == "MOVE" or action_name == "JUMP":
            return (action_name, (start_position, destination))
        elif action_name == "EXIT":
            return (action_name, start_position)
        else:
            # "PASS" action
            return (action_name, None)

    def get_start_positions(self):
        # TODO: if red, start pieces = [...], etc.
        start_positions = {}

        start_positions["red"] = frozenset([(-3, 0), (-3, 1), 
                                            (-3, 2), (-3, 3)])
        start_positions["blue"] = frozenset([(3, 0), (2, 1), 
                                             (1, 2), (0, 3)])
        start_positions["green"] = frozenset([(0, -3), (1, -3), 
                                              (2, -3), (3, -3)])
        # TODO: Testing purpose
        # start_positions["blue"] = frozenset([])
        # start_positions["green"] = frozenset([])

        return start_positions

    def get_exit_positions(self):
        exit_positions = {}

        exit_positions["red"] = [(3, -3), (3, -2), (3, -1), (3, 0)]
        exit_positions["green"] = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
        exit_positions["blue"] = [(-3, 0), (-2, -1), (-1, -2), (0, -3)]

        return exit_positions

    # compute the sum of the distances from all pieces to their closest goals
    # Input: current_state: the current state of the game
    # Output: the sum of the distances from all pieces to their closest goals
    def manhattan_heuristic(self, current_state, colour):
        # current_state["position"] is frozenset, convert it back to a list
        positions = current_state.get_pieces(colour)

        heuristic = 0
        for position in positions:
            # assuming all moves are jump (move distance = 2), + 1 exit action
            heuristic += (self.game_board.manhattan_distance(
                                                    position, colour) / 2 + 1)

        return heuristic

    def get_state_reward(self, game_state):
        # TODO: number of pieces in our team: 10
        # TODO: number of exits: 10
        # TODO: total distances to the goal (h-value): - distances
        state_rewards = {}
        current_pieces = game_state.get_current_pieces()
        number_of_exits = game_state.get_number_of_exits()

        for colour, pieces in current_pieces.items():
            state_rewards[colour] = len(pieces) * \
                        self.reward_of_number_of_pieces(game_state, colour)
            state_rewards[colour] -= self.manhattan_heuristic(
                                                        game_state, colour)

        for colour, exits in number_of_exits.items():
            state_rewards[colour] += exits * self.reward_of_exits(
                                                        game_state, colour)

        return state_rewards

    def reward_of_number_of_pieces(self, game_state, colour):
        number_of_my_pieces = len(game_state.get_pieces(colour))
        number_of_enemy_pieces = len(game_state.get_enemy_pieces(colour, True))

        if number_of_my_pieces == 0 or number_of_enemy_pieces == 0:
            return 0

        return (5 / (number_of_my_pieces / number_of_enemy_pieces))

    def reward_of_exits(self, game_state, colour):
        number_of_my_pieces = len(game_state.get_pieces(colour))
        number_of_exits = game_state.get_number_of_exits()[colour]

        if number_of_exits + number_of_my_pieces >= 4:
            return 15
        else:
            return -5
    
    #check if our piece is next to a enemy's piece, who's got the next turn
    def in_danger(self, colour):
        game_board = self.game_board.get_game_board()
        my_pieces = self.game_state.get_my_pieces()
        next_player_pieces = self.game_state.get_next_player_pieces(colour)

        for position in game_board:
            for piece in my_pieces:
                if position in next_player_pieces and \
                    game_board.jump(position, piece): 
                    return True

        return False
