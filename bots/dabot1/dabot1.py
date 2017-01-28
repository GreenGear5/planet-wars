#!/usr/bin/env python
"""
SuppressBot - It essentially does a form of suppress fire to swamp only the enemy, works particularly well
as a form of defence. For instance, minimax and alphabeta decide that the best choice is to not make
a move at all, resulting in some sort of equilibrium where the game results in a draw.
"""

# Import the API objects
import api.util as u
from api import State

import random, sys


class Bot:
    def __init__(self):
        pass

    def get_move(self, state):

        # Find out which player we are
        my_id = state.whose_turn()
        enemy_id = None

        if my_id == 1:
            enemy_id = 2
        elif my_id == 2:
            enemy_id = 1

        # Our move: these will contain Planet objects

        # Pick least vulnerable planet
        my_planets = state.planets(my_id)
        my_max_n_ships = 0
        source = None

        for planet in my_planets:
            curn = state.garrison(planet)
            if curn > my_max_n_ships:
                my_max_n_ships = curn
                source = planet

        if source is None:
            return None

        # Pick closest enemy planet
        # if take_risk(0.90):
        #     target_planets = state.planets(0)
        # else:
        target_planets = state.planets(enemy_id)
        clodest = 9999
        dest = None

        for planet in target_planets:
            curdist = u.distance(source, planet)
            if curdist < clodest:
                dest = planet

        if dest is None:
            return None

        return source.id(), dest.id()


def take_risk(p):  # where p is between 0 and 1
    r = random.uniform(0, 1)
    if r >= p:
        return True
    else:
        return False

