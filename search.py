"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Zheping Liu, Alisha
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
    #   colour: declaring which colour the palyer is playing, default to be "red"
    #   pieces: specifying the starting position of the player's piece(s), default number is one
    #   blocks: specifying the position of any blocks on 
    with open(sys.argv[1]) as file:
        data = json.load(file)

    start_state = make_state(data["pieces"], None, data["blocks"], None, data["colour"])

    # Search for and output winning sequence of moves
    actions = a_star(start_state)
    print(actions)

# search function body for dfs, bfs and ucs
# def search(open_list, closed_list, data):
#     start_state = {data["position"], None, data["block"], None, data["colour"]}
#     open_list.push(start_state)

#     while not open_list.isEmpty():
#         # pop a state from openList
#         current_state = open_list.pop()

#         if is_goal(current_state):
#             return current_state

#         if not current_state["position"] in closed_list:
#           # add the current state into visited
#           closed_list.append(current_state["position"])
#           for successor in generate_successor(current_state):
#               open_list.push(successor)

#     return None

def make_state(pieces, action, block, previous_state, colour):
    if pieces == None:
        return None
    else:
        new_pieces = []
        # new_piece = (0, 0)
        for piece in pieces:
            q = piece[0]
            r = piece[1]
            new_pieces.append((q, r))
            # new_piece = (q, r)
        
        new_pieces = frozenset(new_pieces)

        current_state = {
                "position": new_pieces,
                # "position": new_piece,
                "action": action,
                "block": block,
                "colour": colour,
                "previous_state": previous_state
        }

        return current_state

def null_heuristic(current_state):
    return 0

def manhattan_distance(position, colour):
    if colour == "red":
        goal = [[3,-3], [3,-2], [3,-1], [3, 0]]
    elif colour == "green":
        goal = [[-3, 3], [-2, 3], [-1, 3], [0, 3]]
    elif colour == "blue":
        goal = [[0, -3], [-1, -2], [-2, -1],[-3, 0]]
        
    #function hex_distance(a, b):
    #return (abs(a.q - b.q) + abs(a.q + a.r - b.q - b.r) + abs(a.r - b.r)) / 2
    dist0 = (abs(position[0] - goal[0][0]) + abs(position[0] + position[1] - goal[0][0] - goal[0][1]) + abs(position[1] - goal[0][1]))/2
    for i in range(1,4):
        temp_dist = (abs(position[0] - goal[i][0]) + abs(position[0] + position[1] - goal[i][0] - goal[i][1]) + abs(position[1] - goal[i][1]))/2
        if temp_dist < dist0:
            dist0 = temp_dist

    return int(dist0)

def manhattan_heuristic(current_state):
    positions = list(current_state["position"])
    colour = current_state["colour"]

    heuristic = 0
    for position in positions:
        heuristic += manhattan_distance(position, colour)
    
    return heuristic

# a star search algorithm
# return a list of actions from start position to goal position
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

    open_list.push(start_state, f_score[start_state['position']])

    while not open_list.is_empty():

        current_state = open_list.pop()
        closed_list.append(current_state["position"])

        # TODO: we have to put the action exit somewhere
        temp_g_score = g_score[current_state["position"]]
        current_state = exit(current_state)
        g_score[current_state["position"]] = temp_g_score

        if is_goal(current_state):
            break

        for successor_state in generate_successor(current_state):
            if successor_state["position"] in closed_list:
                continue

            # the cost to get to current successor is the cost to get to
            # currentState + successor cost
            temp_g_score = g_score[current_state['position']] + COST
            temp_f_score = temp_g_score + \
                heuristic(successor_state)

            # if the gScore for current successor is not recorded, i.e. equals to infinity
            if (successor_state["position"] in g_score.keys()
                    and temp_g_score >= g_score[successor_state["position"]]):
                continue
            else:
                open_list.push(successor_state, temp_f_score)
                g_score[successor_state["position"]] = temp_g_score

    return construct_goal_actions(current_state)


def construct_goal_actions(current_state):

    if current_state == None:
      print("No solution found")
      return []

    # list of actions from start to goal
    goal_actions = []

    # re-construct the actions from goal to start
    while current_state["action"]:
      #print(currentState)
      goal_actions.append(current_state["action"])
      current_state = current_state["previous_state"]

    # return the reverse the goalAction list
    return list(reversed(goal_actions))

# generate successor states for a particular state
def generate_successor(current_state):
    successor = []
    current_positions = current_state['position']
    game_board = get_game_board()
    
    for position in game_board:
        for current_position in current_positions:
            if (position in current_state['block']) and (next_to(current_position, position)):
                # generate all successors with action JUMP
                action = get_action("JUMP", current_position, position)
                new_positions = [x for x in current_positions if x != current_position]
                new_positions.append(position)
                successor.append(make_state(new_positions, action,
                                            current_state['block'], current_state, 
                                            current_state["colour"]))

            elif not position in current_state['block'] and next_to(current_position, position):
                # generate all successors with action MOVE
                action = get_action("MOVE", current_position, position)
                new_positions = [x for x in current_positions if x != current_position]
                new_positions.append(position)
                successor.append(make_state(new_positions, action, 
                                            current_state['block'], current_state,
                                            current_state["colour"]))
    
    return successor


def get_action(action_name, position_1, position_2):
    if not position_2 == None:
        return "%s from %s to %s." % (action_name, position_1, position_2)
    else:
        return "%s from %s." % (action_name, position_1)

def next_to(position_1, position_2):
    (q1, r1) = position_1
    (q2, r2) = position_2

    if q1 == q2 and abs(r1 - r2) == 1:
        # same column case
        return True
    elif r1 == r2 and abs(q1 - q2) == 1:
        # same row case
        return True
    elif abs(r1 - r2) == 1 and abs(q1 - q2) == 1 and \
        (r1 - r2) + (q1 - q2) == 0:
        # third case, e.g. (0, -3) and (-1, -2)
        return True

    return False

def jump(position, block):
    (q1, r1) = position
    (q2, r2) = block

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

    if r <= 3 and r >= -3 and q <= 3 and r >= -3:
        # when the tile is out of range, return empty
        return (q, r)
    
    return None

# action exit
# precondition: any of the chess is at the goal position
# postcondition: remove one of the chess satisfy the precondition from the board,
#                and add an action "EXIT from (x, y)."
def exit(current_state):
    colour = current_state["colour"]
    positions = list(current_state["position"])

    for position in positions:
        if colour == "red":
            if position == (3, -3) or \
                position == (3, -2) or \
                position == (3, -1) or \
                position == (3, 0):
                action = get_action("EXIT", position, None)
                positions.remove(position)
                new_state = make_state(positions, 
                    action, current_state["block"], current_state, colour)
                print(new_state)
                return new_state
            else:
                return current_state
        
        elif colour == "green":
            if position == (-3, 3) or \
                position == (-2, 3) or \
                position == (-1, 3) or \
                position == (0, 3):
                action = get_action("EXIT", position, None)
                positions.remove(position)
                new_state = make_state(positions, 
                    action, current_state["block"], current_state, colour)
                return new_state
            else:
                return current_state
        
        elif colour == "blue":
            if position == (0, -3) or \
                position == (-1, -2) or \
                position == (-2, -1) or \
                position == (-3, 0):
                action = get_action("EXIT", position, None)
                positions.remove(position)
                new_state = make_state(positions, 
                    action, current_state["block"], current_state, colour)
                return new_state
            else:
                return current_state

def is_goal(current_state):
    positions = list(current_state["position"])

    if len(positions) == 0:
        return True

    return False

def get_game_board():
    ran = range(-3, 4)
    game_board = [(q, r) for q in ran for r in ran if -q-r in ran]

    return game_board

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
