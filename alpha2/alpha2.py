#!/usr/bin/env python
"""


"""

from api import State, util
import random

class Bot:

    __max_depth = -1
    __randomize = True

    def __init__(self, randomize=True, depth=4):
        self.__randomize = randomize
        self.__max_depth = depth

    def get_move(self, state):
        val, move = self.value(state)

        return move # to do nothing, return None

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """
        Return the value of this state and the associated move
        :param State state:
        :param float alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param float beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param int depth: How deep we are in the tree
        :return val, move: the value of the state, and the best move.
        """
        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return heuristic(state)

        best_value = float('-inf') if maximizing(state) else float('inf')
        best_move = None

        moves = state.moves()

        if self.__randomize:
            random.shuffle(moves)

        for move in moves:

            next_state = state.next(move)
            value, m = self.value(next_state, alpha, beta, depth + 1)

            if maximizing(state):
                if value > best_value:
                    best_value = value
                    best_move = move
                    alpha = best_value
            else:
                if value < best_value:
                    best_value = value
                    best_move = move
                    beta = best_value

            # Prune the search tree
            # We know this state will never be chosen, so we stop evaluating its children
            if beta <= alpha:
                break

        return best_value, best_move

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).

    :param state:
    :return:
    """
    return state.whose_turn() == 1

def heuristic(state):
    my_id = state.whose_turn()
    if my_id is 1:
        other_id = 2
    else:
        other_id = 1

    source_array = state.planets(my_id)
    dest_array = state.planets(other_id)




    feature_vector = features(state)
    my_array = [0,0,0,0]
    for i in range(0,4):
        my_array[i] = feature_vector.pop()
    ships1 = (my_array[3]+my_array[1])
    ships2 = (my_array[2]+my_array[0])



    gen_1 = resource_rate(state,state.planets(1))
    gen_2 = resource_rate(state,state.planets(2))

    if ships1 > 2 * ships2:
        return pow(1000,ships1/ships2)/(my_array[2]+0.00001),None

    return 10*(ships1)/(ships1+ships2) + 10*gen_1/(gen_1+gen_2), None

def features(state):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """

    # How many ships does p1 have in garrisons?
    p1_garrisons = 0.0
    # How many ships does p2 have in garrisons?
    p2_garrisons = 0.0

    player1_planets = state.planets(1)
    player2_planets = state.planets(2)

    for i in range(0, len(player1_planets)):
        p1_garrisons = p1_garrisons + state.garrison(player1_planets[i])
    for i in range(0, len(player2_planets)):
        p2_garrisons = p2_garrisons + state.garrison(player2_planets[i])

    # How many ships does p1 have in fleets?
    p1_fleets = 0.0
    # How many ships does p2 have in fleets?
    p2_fleets = 0.0


    all_fleets = state.fleets()
    str_fleets = str(all_fleets) #I like working with strings, so cast this.
    for i in range (0,len(all_fleets)):
        str_fleet = str(all_fleets[i]) #Looping through all fleets
        if "o1" in (str_fleets):  #Checks if fleet is player 1 or 2
            temp = str_fleet.split("d", 1)[1] #Tricky bit, returns all characters afer the 'd' (this leaves "someNumber]")
            number = int(temp[0:len(temp)-1])  #Removes "]" and casts to int
            p1_fleets = p1_fleets + int(temp[0:len(temp)-1]) #addition
        if "o2" in (str_fleets):
            temp = str_fleet.split("d", 1)[1] #Same stuff, but for player 2
            number = int(temp[0:len(temp)-1])
            p2_fleets = p2_fleets + int(temp[0:len(temp)-1])
    my_array = [p1_garrisons, p2_garrisons, p1_fleets, p2_fleets]
    return my_array

def resource_rate(state,planet_array):
    array = [None] * len(planet_array)
    rate = 0
    for i in range(0,len(planet_array)):
        rate = rate + planet_array[i].size()
    return rate

def index_of_strongest_planet(state,planet_array):
    temp = 1
    temp_index = -1
    for i in range(0, len(planet_array)):
        if state.garrison(planet_array[i]) > temp:
            temp = state.garrison(planet_array[i])
            temp_index = i
    if temp_index is -1:
        return None
    return planet_array[temp_index].id()

def index_of_biggest_planet(state,planet_array):
    temp = 0
    temp_index = -1
    for i in range(0, len(planet_array)):
        planet = planet_array[i]
        if planet.size() > temp:
            temp = planet.size()
            temp_index = i
    if temp_index is -1:
        return original
    return planet_array[temp_index].id()
