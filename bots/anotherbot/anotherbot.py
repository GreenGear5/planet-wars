#!/usr/bin/env python

"""
RandomBot -- A simple strategy: enumerates all legal moves, and picks one
uniformly at random.
"""

# Import the API objects
from api import State
import random


def index_of_strongest_planet(state,planet_array): # returns the index of the strongest planet from planet_array
    temp = 1
    temp_index = -1
    for i in range(0, len(planet_array)):
        if state.garrison(planet_array[i]) > temp:
            temp = state.garrison(planet_array[i])
            temp_index = i
    if temp_index is -1:
        return None
    return planet_array[temp_index].id()

# returns the index of the biggest planet from planet_array, if the planet_array is empty, orginal is returned as destination
def index_of_biggest_planet(state,planet_array,original):
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

class Bot:

    def __init__(self):
        pass

    def get_move(self, state):
        # type: (State) -> tuple[int, int]
        """
        Function that gets called every turn. This is where to implement the strategies.

        Be sure to make a legal move. Illegal moves, like giving a source planet you
        don't own, will lose you the game.

        If you return a source and destination, 50% of the ships of the source
        planet (rounded down) will be sent to the destination. If that planet is
        owned by the enemy or neutral when they arrive, they will attack it, if it is
        owned by you, they will reinforce it (add to the number of ships stationed).

        :param State state: An object representing the gamestate. This includes a link to the
            map, ownership of each planet, garrisons on each plant, and all fleets in transit.

        :return: None, indicating no move is made, or a pair of integers,
            indicating a move; the first indicates the source planet, the second the
            destination.
        """

        my_id = state.whose_turn()
        if my_id is 1:
            other_id = 2
        else:
            other_id = 1

        if len(state.fleets()) > 0:
            print(state.fleets()[0])

        return None

