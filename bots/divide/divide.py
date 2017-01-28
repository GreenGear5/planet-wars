#!/usr/bin/env python
"""
SuppressBot - It essentially does a form of suppress fire to swamp only the enemy, works particularly well
as a form of defence. For instance, minimax and alphabeta decide that the best choice is to not make
a move at all, resulting in some sort of equilibrium where the game results in a draw.
"""

# Import the API objects
import api.util as u
from api import State, util

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
        try:
            source = random.choice(state.planets(my_id))  # Pick randomly from our planets.
            dest = random.choice(state.planets(enemy_id))  # Pick randomly from their planets.
        except IndexError:
            return None

        my_planets = state.planets(my_id)
        other_planets = state.planets(0)

        #for i in range (0,len(my_planets))


        print(util.distance(source,dest))

        if source is None or dest is None:
            return None
        # Keep in mind, we never fire at neutrals since they don't pose immediate danger.
        return source.id(), dest.id()
