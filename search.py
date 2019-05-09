"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Zheping Liu, 683781; Bohan Yang, 814642
"""

import sys
import json
import heapq

# A Priority queue implemented using heapq
# Reference: https://segmentfault.com/a/1190000010007858
class PriorityQueue:
    def __init__(self):
        self._index = 0
        self._queue = []
        self.size = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (priority, self._index, item))
        self._index += 1
        self.size += 1

    def pop(self):
        self.size -= 1
        return heapq.heappop(self._queue)[-1]

    def is_empty(self):
        return self.size == 0

def main():
    # the file contains three entries:
    #   colour: declaring which colour the palyer is playing, 
    #           default to be "red"
    #   pieces: specifying the starting position of the player's piece(s), 
    #           default number is one
    #   blocks: specifying the position of any blocks on 
    with open(sys.argv[1]) as file:
        data = json.load(file)

    # make the initial state using the contents in data file,
    # where "action" and "previous_state" are left with None
    start_state = make_state(data["pieces"], None, data["blocks"], 
                             None, data["colour"])

    # Search for and output winning sequence of moves
    actions = a_star(start_state, manhattan_heuristic)
    print_goal_actions(actions)

# make a game state
# Input: pieces: the existing pieces on the game board
#        action: last action performed
#        blocks: the existing blocks on the game board
#        previous_state: previous game state
#        colour: the colour of our pieces
# Output: a game state represented by a dict with 5 attributes
def make_state(pieces, action, blocks, previous_state, colour):
    # if there are no pieces specified, return None
    if pieces == None:
        return None
    else:
        new_pieces = []
        # convert coordinates of all pieces to tuple form, i.e. (q, r)
        for piece in pieces:
            q = piece[0]
            r = piece[1]
            new_pieces.append((q, r))

        # convert coordinates of all pieces to tuple form, i.e. (q, r)
        new_blocks = []
        for block in blocks:
            q = block[0]
            r = block[1]
            new_blocks.append((q, r))
        
        # convert the list of pieces to a frozenset (frozenset is hashable)
        new_pieces = frozenset(new_pieces)
        # make the state
        current_state = {
                "position": new_pieces,
                # "position": new_piece,
                "action": action,
                "block": new_blocks,
                "colour": colour,
                "previous_state": previous_state
        }
        return current_state

# null heuristic that always return 0, with this heuristic, a_star will perform
# exactly the same as BFS
def null_heuristic(current_state):
    return 0

# compute the manhattan distance from a piece to its closest goal on
# the hex game board 
# Input: position: the coordinate of a piece
#        colour: the colour of the input piece
# Output: the shortest distance between the piece and the goal
def manhattan_distance(position, colour):
    if colour == "red":
        goal = [[3,-3], [3,-2], [3,-1], [3, 0]]
    elif colour == "green":
        goal = [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
    elif colour == "blue":
        goal = [[0, -3], [-1, -2], [-2, -1],[-3, 0]]
        
    dist0 = (abs(position[0] - goal[0][0]) + abs(position[0] + position[1] 
            - goal[0][0] - goal[0][1]) + abs(position[1] - goal[0][1])) / 2

    # take the minimum distance (to make sure the heuristic is admissible) from
    # distances to all goals
    for i in range(1,4):
        temp_dist = (abs(position[0] - goal[i][0]) + abs(position[0] 
                    + position[1] - goal[i][0] - goal[i][1]) + 
                    abs(position[1] - goal[i][1])) / 2
        if temp_dist < dist0:
            dist0 = temp_dist

    return int(dist0)

# compute the sum of the distances from all pieces to their closest goals
# Input: current_state: the current state of the game
# Output: the sum of the distances from all pieces to their closest goals
def manhattan_heuristic(current_state):
    # current_state["position"] is frozenset, convert it back to a list
    positions = list(current_state["position"])
    colour = current_state["colour"]

    heuristic = 0
    for position in positions:
        # assuming all moves are jump (move distance = 2), + 1 exit action
        heuristic += (manhattan_distance(position, colour) / 2 + 1)
    
    return heuristic

# A-star search algorithm
# Input: start_state: the initial state of the game
#        heuristic: the given heuristic for A-star
# Output: a list of actions to move all pieces out of the game board
def a_star(start_state, heuristic=null_heuristic):
    COST = 1
    # priority queue of states to be visited
    open_list = PriorityQueue()
    # list of expanded coordinates
    closed_list = []
    # dict of coordinates correspond to the cost from start to it
    g_score = {}
    # dict of coordinates correspond to the total cost to go to the goal
    # from start by passing through this coordinate
    f_score = {}

    g_score[start_state["position"]] = 0
    f_score[start_state["position"]] = heuristic(start_state)

    open_list.push(start_state, f_score[start_state["position"]])

    while not open_list.is_empty():
        current_state = open_list.pop()
        closed_list.append(current_state["position"])

        # if the goal is achieved, break the loop
        if is_goal(current_state):
            return construct_goal_actions(current_state)


        for successor_state in generate_successor(current_state):
            # skip if the same combination of pieces coordinates has already
            # been visited
            # if successor_state["position"] in closed_list:
            if successor_state in closed_list:
                continue

            # the cost to get to current successor is the cost to get to
            # currentState + successor cost
            temp_g_score = g_score[current_state["position"]] + COST
            temp_f_score = temp_g_score + heuristic(successor_state)

            if successor_state["position"] not in g_score or g_score[successor_state["position"]] > temp_g_score:
                open_list.push(successor_state, temp_f_score)
                g_score[successor_state["position"]] = temp_g_score

    return construct_goal_actions(current_state)


# construct the list of actions from the start state to the given game state
# Input: game_state: the given game state
# Output: a list of actions from the start state to the give game state
def construct_goal_actions(game_state):
    if game_state == None:
      print("No solution found")
      return []

    # list of actions from start to goal
    goal_actions = []

    # re-construct the actions from goal to start
    while game_state["action"]:
      #print(currentState)
      goal_actions.append(game_state["action"])
      game_state = game_state["previous_state"]

    # return the reverse the goalAction list
    return list(reversed(goal_actions))

def generate_successor(game_state):
    exit_successors = generate_exit_successor(game_state)
    jump_successors = generate_jump_successor(game_state)
    move_successors = generate_move_successor(game_state)

    successor = exit_successors + jump_successors + move_successors

    return successor

def generate_exit_successor(game_state):
    exit_successors = []
    current_pieces = game_state["position"]

    for piece in current_pieces:
        if is_sub_goal(piece, game_state["colour"]):
            new_pieces = [x for x in current_pieces if x != piece]
            action = get_action("EXIT", piece, None)
            exit_successors.append(make_state(new_pieces, action, 
                                        game_state["block"], game_state, 
                                        game_state["colour"]))

    return exit_successors

def generate_jump_successor(game_state):
    jump_successors = []
    current_pieces = game_state["position"]
    occupied_pieces = list(game_state["position"]) + game_state["block"]

    for position in occupied_pieces:
        for piece in current_pieces:
            if next_to(position, piece):
                jump_destination = jump(piece, position)
                if jump_destination[0] and \
                    jump_destination[1] not in occupied_pieces:
                    jump_destination = jump_destination[1]
                    action = get_action("JUMP", piece, jump_destination)
                    new_pieces = [x for x in current_pieces if x != piece]
                    new_pieces.append(jump_destination)
                    jump_successors.append(make_state(new_pieces, action,
                                                game_state["block"], game_state,
                                                game_state["colour"]))

    return jump_successors

def generate_move_successor(game_state):
    move_successors = []
    current_pieces = game_state["position"]
    occupied_pieces = list(game_state["position"]) + game_state["block"]
    game_board = get_game_board()

    for position in game_board:
        for piece in current_pieces:
            if position not in occupied_pieces and \
                next_to(position, piece):
                action = get_action("MOVE", piece, position)
                new_pieces = [x for x in current_pieces if x != piece]
                new_pieces.append(position)
                move_successors.append(make_state(new_pieces, action,
                                            game_state["block"], game_state,
                                            game_state["colour"]))

    return move_successors

# generate the action in the specified format
# Input: action_name: name of the action, includes "MOVE", "JUMP", "EXIT"
# Output: the action in specified format
def get_action(action_name, position_1, position_2):
    if not position_2 == None:
        # generate MOVE and JUMP action
        return "%s from %s to %s." % (action_name, position_1, position_2)
    else:
        # generate EXIT action
        return "%s from %s." % (action_name, position_1)

# check if two positions are next to each other on the hex game board
# Input: position_1: given position 1
#        position_2: given position 2
# Output: True if they are next to each other, otherwise False
def next_to(position_1, position_2):
    HEX_STEPS = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
    (q1, r1) = position_1
    (q2, r2) = position_2

    for step_q, step_r in HEX_STEPS:
        if (q1 + step_q, r1 + step_r) == (q2, r2):
            return True

    return False

# generate the successor coordinate for a piece to JUMP through a block
# Input: position: the coordinate of the given piece
#        block: the coordinate of the given block
def jump(position, block):
    # HEX_STEPS = [(-1, 0), (0, -1), (1, -1), (1, 0), (0, 1), (-1, 1)]
    SENTINEL = -4
    (q1, r1) = position
    (q2, r2) = block
    q = SENTINEL
    r = SENTINEL
    if q1 == q2 and r1 - r2 == 1:
        q = q1
        r = r2 - 1
    elif q1 == q2 and r1 - r2 == -1:
        q = q1
        r = r2 + 1
    elif r1 == r2 and q1 - q2 == 1:
        q = q2 - 1
        r = r1
    elif r1 == r2 and q1 - q2 == -1:
        q = q2 + 1
        r = r1
    elif q1 - q2 == -1 and r1 - r2 == 1:
        # e.g. (-1,0) and (0,-1)
        q = q1 + 2
        r = r1 - 2
    elif r1 - r2 == -1 and q1 - q2 == 1:
        # e.g. (2,1) and (1,2)
        q = q1 - 2
        r = r1 + 2

    # check if the generated position is in the valid range
    if (q, r) in get_game_board():
        return (True, (q, r))
    
    # when the tile is out of range, return empty
    return (False, None)

# check if the piece has arrived at the goal position (achieve the sub-goal
# of the game)
# Input: piece: the specified piece
#        colour: the colour of the specified piece
# Output: return True if the given piece is at any of the goal position,
#         otherwise return False
def is_sub_goal(piece, colour):
    if colour == "red":
        goal = [(3, -3), (3, -2), (3, -1), (3, 0)]
    elif colour == "green":
        goal = [(-3, 3), (-2, 3), (-1, 3), (0, 3)]
    elif colour == "blue":
        goal = [(0, -3), (-1, -2), (-2, -1), (-3, 0)]

    if piece in goal:
        return True
    
    return False

# check if the given game state is the goal state (no pieces on the board)
# Input: game_state: the given game state
# Output: True if there is no pieces left on the board, False otherwise.
def is_goal(game_state):
    positions = list(game_state["position"])

    if len(positions) == 0:
        return True

    return False

# get all valid coordinates on the game board
def get_game_board():
    ran = range(-3, 4)
    game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

    return game_board

# print the winning actions according to the specified format
def print_goal_actions(actions):
    for action in actions:
        print(action)
    print("# Total number of moves is %d" % (len(actions)))
    return

def print_board(board_dict, message="", debug=False, **kwargs):
    """
    Helper function to print a drawing of a hexagonal board's contents.
    
    Arguments:

    * `board_dict` -- dictionary with tuples for keys and anything printable
    for values. The tuple keys are interpreted as hexagonal coordinates (using 
    the axial coordinate system outlined in the project specification) and the 
    values are formatted as strings and placed in the drawing at the corres- 
    ponding location (only the first 5 characters of each string are used, to 
    keep the drawings small). Coordinates with missing values are left blank.

    Keyword arguments:

    * `message` -- an optional message to include on the first line of the 
    drawing (above the board) -- default `""` (resulting in a blank message).
    * `debug` -- for a larger board drawing that includes the coordinates 
    inside each hex, set this to `True` -- default `False`.
    * Or, any other keyword arguments! They will be forwarded to `print()`.
    """

    # Set up the board template:
    if not debug:
        # Use the normal board template (smaller, not showing coordinates)
        template = """# {0}
#           .-'-._.-'-._.-'-._.-'-.
#          |{16:}|{23:}|{29:}|{34:}| 
#        .-'-._.-'-._.-'-._.-'-._.-'-.
#       |{10:}|{17:}|{24:}|{30:}|{35:}| 
#     .-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
#    |{05:}|{11:}|{18:}|{25:}|{31:}|{36:}| 
#  .-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-.
# |{01:}|{06:}|{12:}|{19:}|{26:}|{32:}|{37:}| 
# '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#    |{02:}|{07:}|{13:}|{20:}|{27:}|{33:}| 
#    '-._.-'-._.-'-._.-'-._.-'-._.-'-._.-'
#       |{03:}|{08:}|{14:}|{21:}|{28:}| 
#       '-._.-'-._.-'-._.-'-._.-'-._.-'
#          |{04:}|{09:}|{15:}|{22:}|
#          '-._.-'-._.-'-._.-'-._.-'"""
    else:
        # Use the debug board template (larger, showing coordinates)
        template = """# {0}
#              ,-' `-._,-' `-._,-' `-._,-' `-.
#             | {16:} | {23:} | {29:} | {34:} | 
#             |  0,-3 |  1,-3 |  2,-3 |  3,-3 |
#          ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
#         | {10:} | {17:} | {24:} | {30:} | {35:} |
#         | -1,-2 |  0,-2 |  1,-2 |  2,-2 |  3,-2 |
#      ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-. 
#     | {05:} | {11:} | {18:} | {25:} | {31:} | {36:} |
#     | -2,-1 | -1,-1 |  0,-1 |  1,-1 |  2,-1 |  3,-1 |
#  ,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-.
# | {01:} | {06:} | {12:} | {19:} | {26:} | {32:} | {37:} |
# | -3, 0 | -2, 0 | -1, 0 |  0, 0 |  1, 0 |  2, 0 |  3, 0 |
#  `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#     | {02:} | {07:} | {13:} | {20:} | {27:} | {33:} |
#     | -3, 1 | -2, 1 | -1, 1 |  0, 1 |  1, 1 |  2, 1 |
#      `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' 
#         | {03:} | {08:} | {14:} | {21:} | {28:} |
#         | -3, 2 | -2, 2 | -1, 2 |  0, 2 |  1, 2 | key:
#          `-._,-' `-._,-' `-._,-' `-._,-' `-._,-' ,-' `-.
#             | {04:} | {09:} | {15:} | {22:} |   | input |
#             | -3, 3 | -2, 3 | -1, 3 |  0, 3 |   |  q, r |
#              `-._,-' `-._,-' `-._,-' `-._,-'     `-._,-'"""

    # prepare the provided board contents as strings, formatted to size.
    ran = range(-3, +3+1)
    cells = []
    for qr in [(q,r) for q in ran for r in ran if -q-r in ran]:
        if qr in board_dict:
            cell = str(board_dict[qr]).center(5)
        else:
            cell = "     " # 5 spaces will fill a cell
        cells.append(cell)

    # fill in the template to create the board drawing, then print!
    board = template.format(message, *cells)
    print(board, **kwargs)


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
