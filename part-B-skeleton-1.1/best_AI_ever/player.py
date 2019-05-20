"""
COMP30024 Artificial Intelligence Project Part B
Team: best_ai_ever
Authors: Zheping Liu, 683781
          Bohan Yang, 814642
"""

from best_AI_ever.game_state import GameState as GameState
from best_AI_ever.game_board import GameBoard as GameBoard
from best_AI_ever.priority_queue import PriorityQueue as PriorityQueue
import copy
import math

class Player:
    """
    Player class that represents players in the game.
    Each Player instance contains the colour of their team, a GameBoard
    instance, and the current game state (a GameState instance).
    """
    def __init__(self, colour):
        """
        Initialise an instance of Player.
        Input: colour: the specified colour for this player 
        """
        self.colour = colour
        self.game_board = GameBoard()

        # initialise the start positions for all players
        start_positions = self.get_start_positions()
        # get the exit positions for all players
        exit_positions = self.get_exit_positions()
        # initialise the number of exits for all players
        number_of_exits = {"red": 0, "green": 0, "blue": 0}
        # initialise the starting game state with inital start positions, exit 
        # positions and number of exits for all teams, None as previous action 
        # and previous state
        self.game_state = GameState(colour, start_positions, 
                                    exit_positions, action=None, 
                                    previous_state=None, number_of_exits=
                                    number_of_exits)

    def action(self):
        """
        Return the optimal action according to the current game state.
        Output: the optimal action at current game state
        """
        ZERO = 0
        ACTION_NAME = 0
        SENTINEL = -1
        # the maximum depth of successor states to look into
        LIMIT = 6
        # the discount factor for discounting rewards in successor states 
        DISCOUNT = 0.8

        # get my desirable successors
        my_desirable_successors = self.get_desirable_successors(self.colour)

        # if no desirable actions are returned, choose the action returns
        # highest reward from all available actions
        if my_desirable_successors == []:
            available_successors = self.generate_successor(self.game_state, 
                                                           self.colour)
            # if there is no available actions, return PASS action
            if available_successors == []:
                return ("PASS", None)
            
            my_desirable_successors = available_successors
        
        # get the colour of next player
        next_player = self.game_state.get_next_player_colour(self.colour)
        # copy the desirable_successors into current_successors
        current_successors = my_desirable_successors[:]
        # generate a list of rewards for successors in current_successors
        state_rewards = [self.get_state_reward(x) for x in current_successors]

        i = ZERO
        # loop till reaching the maximum depth
        while i < LIMIT:
            next_player_successors = []
            for j in range(len(current_successors)):
                successor = current_successors[j]
                # generate the optimal successor for the next player
                next_player_successors.append(self.choose_optimal_successor(
                                                successor, next_player))
                # get the colour of next player
                next_player = self.game_state.get_next_player_colour(
                                                next_player)
                # add the discounted reward of the successors to their
                # respective current state
                state_rewards[j][self.colour] += math.pow(DISCOUNT, i+1) * \
                                self.get_state_reward(successor)[self.colour]

            current_successors = next_player_successors
            i += 1
        
        max_reward = ZERO
        max_reward_index = SENTINEL
        # find the current state with the maximum state rewards (including
        # their respective successors), and return the action applied in
        # this state
        for i in range(len(current_successors)):
            if state_rewards[i][self.colour] > max_reward:
                max_reward = state_rewards[i][self.colour]
                max_reward_index = i
            # if more than one states have the same state rewards, the state
            # with JUMP action is preferred
            elif state_rewards[i][self.colour] == max_reward and \
                current_successors[i].get_action()[ACTION_NAME] == "JUMP":
                max_reward_index = i

        action = my_desirable_successors[max_reward_index].get_action()
        return action

    def update(self, colour, action):
        """
        Updating the current game state.
        Input: colour: the colour of the current player
               action: the action applied by the current player
        """
        self.game_state.update(colour, action)
        return

    def choose_optimal_successor(self, game_state, colour):
        """
        Choosing the optimal successor by removing all undesirable
        actions and finding all urgent actions. If there is any urgent
        action, choose the one return the highest state reward from the urgent
        action lists; otherwise, choose the one return the highest state reward
        from the desirable action lists.
        Input: game_state: the current game state
               colour: the colour of the current player
        Output: the successor state with the highest state reward
        """
        ZERO = 0
        ACTION_NAME = 0
        SENTINEL = -1

        # return all available successors
        available_successors = self.generate_successor(game_state, self.colour)

        # return the successor with Pass action when no other actions available
        if available_successors == []:
            return self.generate_new_game_state(game_state, 
                        game_state.get_current_pieces(), ("PASS", None))

        # get all desirable successors
        desirable_successors = self.get_desirable_successors(self.colour)
        
        # when there is no desirable successors, choose the one with highest
        # state rewards among all available successors
        if desirable_successors == []:
            r_max = ZERO
            r_max_index = SENTINEL
            for i in range(len(available_successors)):
                r_successor = self.get_state_reward(available_successors[i])
                if r_successor[colour] > r_max:
                    r_max = r_successor[colour]
                    r_max_index = i
                elif r_successor[colour] == r_max:
                    if available_successors[i].get_action()[ACTION_NAME] == \
                                                            "JUMP":
                        r_max_index = i
            
            return available_successors[r_max_index]

        # choose the successor that returns highest state rewards
        r_max = ZERO
        r_max_index = SENTINEL
        for i in range(len(desirable_successors)):
            r_successor = self.get_state_reward(desirable_successors[i])
            if r_successor[colour] > r_max:
                r_max = r_successor[colour]
                r_max_index = i

        return desirable_successors[r_max_index]
    
    def get_desirable_successors(self, colour):
        """
        Get all desirable successors for the given player at current state
        Input: colour: the colour of the player
        Output: a list of desirable successors at current state
        """
        ACTION_POSITIONS = 1
        PRE_POSITION = 0
        AFTER_POSITION = 1

        # get all available successors and their respective actions
        available_successors = self.generate_successor(
                                    self.game_state, colour)
        available_actions = [x.get_action() for x in available_successors]

        desirable_actions = available_actions
        desirable_successors = available_successors
        urgent_successors = []
        
        # get all pieces for the given player that are protecting other
        # pieces of that player
        protecting_pieces = self.game_state.is_protecting_pieces()

        # get all positions that could be occupied to form protection for
        # other pieces of that player
        protection_positions = self.game_state.get_protection_positions()

        # get all pieces are in danger (could be acquired by enemy)
        risky_pieces = self.game_state.get_risky_pieces()
        
        # iterating through all successor and their respective actions
        for successor, successor_action in zip(available_successors,
                                               available_actions):
            # Exit actions are always desirable
            if successor_action[0] == 'EXIT':
                continue

            pre_position = successor_action[ACTION_POSITIONS][PRE_POSITION]
            after_position = successor_action[ACTION_POSITIONS][AFTER_POSITION]

            # if the after move position can form protection to other pieces
            # or if the pre move position is in danger, add the action to
            # urgent action list
            if after_position in protection_positions or \
                pre_position in risky_pieces:
                urgent_successors.append(successor)

            # if the pre move position is protecting other pieces (applying
            # this action will make our other piece become risky), remove it
            # from the desirable action list
            if pre_position in protecting_pieces:
                desirable_actions = [x for x in desirable_actions
                                     if x != successor_action]
                desirable_successors = [x for x in desirable_successors
                                        if x != successor]
                continue

            # iterating through enemy pieces in successor states, if some
            # enemy pieces are acquired by us this turn, it would not be an
            # enemy piece in the successor state
            for enemy in successor.get_enemy_pieces(self.colour, True):
                # if the distance after applying the successor action is below
                # 2, i.e. distance = 1, remove this action from the desirable
                # action list
                if (self.game_board.hex_distance(after_position, enemy) < 2 and
                    not self.game_board.no_jump_for_enemy(successor, 
                    after_position, enemy)):
                    desirable_actions = [x for x in desirable_actions
                                         if x != successor_action]
                    desirable_successors = [x for x in desirable_successors
                                            if x != successor]

        # remove all undesirable successors in urgent successors
        urgent_successors = [x for x in urgent_successors 
                             if x in desirable_successors]

        # if there is any urgent successor, return it
        if urgent_successors != []:
            return urgent_successors

        # otherwise, return the desirable successors
        return desirable_successors

    def a_star_search(self, game_state, colour):
        """
        A* algorithm that searches the optimal path to the goal for the
        given player at given game state
        Input: game_state: current game state
               colour: the colour of the given player
        Output: list of actions from current game_state to goal state
        """
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
        """
        Generate all successor states for the given player in the given
        game state.
        Input: game_state: given current game state
               colour: the colour of the given player
        Output: a list of successors for the given player in the given game
                state
        """
        exit_successors = self.generate_exit_successor(game_state, colour)
        jump_successors = self.generate_jump_successor(game_state, colour)
        move_successors = self.generate_move_successor(game_state, colour)

        successors = exit_successors + jump_successors + move_successors

        # remove the duplicate successors
        return list(set(successors))

    def generate_exit_successor(self, game_state, colour):
        """
        Generate all successors by applying EXIT action for the given player
        in the given game state.
        Input: game_state: given current game state
               colour: the colour of the given player
        Output: a list of successors with action EXIT for the given playe
                in the given game state
        """
        exit_successors = []
        current_pieces = game_state.get_current_pieces()

        # iterating through all pieces of the given player in the given game
        # state
        for piece in current_pieces[colour]:
            # if the piece is at the exit position
            if game_state.is_sub_goal(piece, colour):
                # make a copy of the current pieces
                new_pieces = copy.deepcopy(current_pieces)
                new_pieces[colour] = frozenset([x for x in 
                                    current_pieces[colour] if x != piece])
                action = self.get_action("EXIT", piece, None)
                # generate the successor game state and add it to the
                # exit_successors
                new_game_state = self.generate_new_game_state(game_state, 
                                                            new_pieces, action)
                exit_successors.append(new_game_state)

        return exit_successors

    def generate_jump_successor(self, game_state, colour):
        """
        Generate all successors by applying JUMP action for the given player
        in the given game state.
        Input: game_state: given current game state
               colour: the colour of the given player
        Output: a list of successors with action JUMP for the given playe
                in the given game state
        """
        JUMP_RESULT = 0
        JUMP_POSITION = 1
        jump_successors = []
        current_pieces = game_state.get_current_pieces()
        # all positions that are occupied in the given game state, including
        # the positions occupied by our pieces
        occupied_positions = game_state.get_occupied_positions()

        for position in occupied_positions:
            for piece in current_pieces[colour]:
                # if an occupied position is next to one of our pieces, and
                # the position beyond it is not occupied, generate a
                # successor with JUMP action
                if self.game_board.next_to(position, piece):
                    # generate the successor coordinate by applying action JUMP
                    jump_destination = self.game_board.jump(piece, position)
                    # if there is a possible JUMP coordinate and this coordinate
                    # is not occupied by other pieces
                    if jump_destination[JUMP_RESULT] and \
                        jump_destination[JUMP_POSITION] 
                        not in occupied_positions:
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
        """
        Generate all successors by applying MOVE action for the given player
        in the given game state.
        Input: game_state: given current game state
               colour: the colour of the given player
        Output: a list of successors with action MOVE for the given playe
                in the given game state
        """
        move_successors = []
        current_pieces = game_state.get_current_pieces()
        occupied_positions = game_state.get_occupied_positions()
        # get all valid positions on the game board
        game_board = self.game_board.get_game_board()

        for position in game_board:
            for piece in current_pieces[colour]:
                # if the position is not occupied and next to our pieces,
                # generate a successor with MOVE action
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
        """
        Generate a successor state from a previous game state.
        Input: pre_game_state: the predecessor game state
               new_pieces: new list of pieces
               action: the action applied to the previous game state
        Output: successor game state with new list of pieces and new action
        """
        ACTION_NAME = 0
        colour = pre_game_state.get_colour()
        exit_positions = pre_game_state.get_exit_positions()
        number_of_exits = pre_game_state.get_number_of_exits().copy()

        # if the action is an EXIT action, increment the number_of_exits for
        # that colour
        if action[ACTION_NAME] == "EXIT":
            number_of_exits[colour] += 1

        return GameState(colour, new_pieces, exit_positions, 
                            action, pre_game_state, number_of_exits)

    def get_action(self, action_name, start_position, destination):
        """
        Generate an action in tuple form, e.g. (MOVE, ((1, 1), (1, 0))).
        Input: action_name: the name of the action
               start_position: the previous position before the action
               destination: the destination after the action, for EXIT action 
                            this will be None
        Output: an action in tuple form
        """
        if action_name == "MOVE" or action_name == "JUMP":
            return (action_name, (start_position, destination))
        elif action_name == "EXIT":
            return (action_name, start_position)
        else:
            # "PASS" action
            return (action_name, None)


    def get_start_positions(self):
        """
        Get the positions of all teams at the begining of the game.
        Output: a dict, where keys are the colours of teams, and the values
                are a frozenset contains all pieces for their respecting team
        """
        start_positions = {}

        start_positions["red"] = frozenset([(-3, 0), (-3, 1), 
                                            (-3, 2), (-3, 3)])
        start_positions["blue"] = frozenset([(3, 0), (2, 1), 
                                             (1, 2), (0, 3)])
        start_positions["green"] = frozenset([(0, -3), (1, -3), 
                                              (2, -3), (3, -3)])

        return start_positions

    def get_exit_positions(self):
        """
        Get the exit positions of all teams.
        Output: a dict, where keys are the colours of teams, and the values
                are a frozenset contains all exit positions for their 
                respecting team
        """
        exit_positions = {}

        exit_positions["red"] = [(3, -3), (3, -2), (3, -1), (3, 0)]
        exit_positions["green"] = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
        exit_positions["blue"] = [(-3, 0), (-2, -1), (-1, -2), (0, -3)]

        return exit_positions

    def get_state_reward(self, game_state):
        """
        Estimating the value of a given game state for all teams:
        rewards = number_of_pieces * value of one piece + 
                  total_distances_to_goal * value of distance +
                  number_of_exits * value of exits
        Input: game_state: given game state
        Output: a dict, contains the reward of all teams at the given game
                state; the colour of different teams are the keys, the values
                are their respective rewards of state
        """
        state_rewards = {}
        current_pieces = game_state.get_current_pieces()
        number_of_exits = game_state.get_number_of_exits()

        for colour, pieces in current_pieces.items():
            # number of pieces * value of pieces, where value of pieces
            # is a function of the ratio between "number of my pieces" and
            # "number of enemy pieces"
            state_rewards[colour] = len(pieces) * \
                        self.reward_of_number_of_pieces(game_state, colour)
            
            # add the value of total distances, this is a negative value,
            # i.e. the shorter the distance, the higher the value
            state_rewards[colour] += self.reward_of_distances(game_state, 
                                          colour) * self.manhattan_heuristic(
                                                  game_state, colour)

        for colour, exits in number_of_exits.items():
            # add the value of the total number of exits
            state_rewards[colour] += exits * self.reward_of_exits(
                                                        game_state, colour)

        return state_rewards

    def reward_of_number_of_pieces(self, game_state, colour):
        '''
        The reward function is a natural logarithm function on the ratio 
        between number of my pieces and number of enemy pieces. As the ratio 
        increase, the marginal reward of capturing new pieces decreases, which
        means it does not encourage capturing more pieces when our pieces
        outnumber the enemies.
        Similarly, if the ratio drops, acquiring new piece will bring much
        higher value.

        Input: game_state: the given game state
               colour: the colour of the given team
        Output: the value of a single piece at the given state for the given
                team
        '''
        number_of_my_pieces = len(game_state.get_pieces(colour))
        number_of_enemy_pieces = len(game_state.get_enemy_pieces(colour, True))

        # if the given team is not at goal, but has no more pieces on the
        # game board, the reward is -200
        if not game_state.is_goal(colour) and number_of_my_pieces == 0:
            return -200
        # if there is no more enemy pieces, the value of pieces is 0
        elif number_of_enemy_pieces == 0:
            return 0

        # in all other cases, the value is the result from the natural
        # logarithm function [-3 * ln(n/m) + 10], where n is the number of
        # pieces, m is the number of enemy pieces
        return (-3 * math.log(number_of_my_pieces / number_of_enemy_pieces)
                + 10)

    def reward_of_exits(self, game_state, colour):
        """
        The reward of one exit.
        Input: game_state: the given game state
               colour: the colour of the given team
        Output: the value of a single exit at the given state for the given
                team
        """
        number_of_my_pieces = len(game_state.get_pieces(colour))
        number_of_exits = game_state.get_number_of_exits()[colour]

        # when the state is at goal, the value of each exit is 100
        if game_state.is_goal(colour):
            return 100
        # when the sum of the number of exits and number of pieces is greater
        # or equal than 4, the value of each exit is 10
        elif number_of_exits + number_of_my_pieces >= 4:
            return 10
        # otherwise, i.e. there is not enough exits and not enough pieces to
        # exit, the value of each exit is -100
        else:
            return -100

    def reward_of_distances(self, game_state, colour):
        """
        The reward of every one distance to the goal.
        Input: game_state: the given game state
               colour: the colour of the given team
        Output: the value of every one distance to the goal at the given state
                for the given team
        """
        number_of_my_pieces = len(game_state.get_pieces(colour))
        number_of_exits = game_state.get_number_of_exits()[colour]

        # when the sum of the number of exits and number of pieces is less
        # than 4, value of distance is 0, i.e. there is no penalty for getting
        # away from the exit positions
        if number_of_exits + number_of_my_pieces < 4:
            return 0
        # otherwise, -2 penalty for each hex away
        else:
            return -2

    def manhattan_heuristic(self, current_state, colour):
        """
        compute the sum of the distances from all pieces to their closest goals
        Input: current_state: the current state of the game
        Output: the sum of the distances from all pieces to their closest goals
        """
        # current_state["position"] is frozenset, convert it back to a list
        positions = current_state.get_pieces(colour)

        heuristic = 0
        for position in positions:
            # assuming all moves are jump (move distance = 2), + 1 exit action
            heuristic += (self.game_board.manhattan_distance(
                position, colour) / 2 + 1)

        return heuristic