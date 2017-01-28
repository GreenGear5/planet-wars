#!/usr/bin/env python
"""
A basic adaptive bot. This is part of the second worksheet.

"""

from api import State, util
import random, os

from sklearn.externals import joblib

DEFAULT_MODEL = os.path.dirname(os.path.realpath(__file__)) + '/model-10000.pkl'

class Bot:

    __max_depth = -1
    __randomize = True

    __model = None

    def __init__(self, randomize=True, depth=4, model_file=DEFAULT_MODEL):

        print(model_file)
        self.__randomize = randomize
        self.__max_depth = depth

        # Load the model
        self.__model = joblib.load(model_file)

    def get_move(self, state):

        val, move = self.value(state)

        return move

    def value(self, state, alpha=float('-inf'), beta=float('inf'), depth = 0):
        """
        Return the value of this state and the associated move
        :param state:
        :param alpha: The highest score that the maximizing player can guarantee given current knowledge
        :param beta: The lowest score that the minimizing player can guarantee given current knowledge
        :param depth: How deep we are in the tree
        :return: val, move: the value of the state, and the best move.
        """
        if state.finished():
            return (1.0, None) if state.winner() == 1 else (-1.0, None)

        if depth == self.__max_depth:
            return self.heuristic(state), None

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
            if alpha < beta:
                break

        return best_value, best_move

    def heuristic(self, state):
        # Convert the state to a feature vector
        feature_vector = [features(state)]

        # These are the classes: ('won', 'lost')
        classes = list(self.__model.classes_)

        # Ask the model for a prediction
        # This returns a probability for each class
        prob = self.__model.predict_proba(feature_vector)[0]
        # print('{} {} {}'.format(classes, prob, util.ratio_ships(state, 1)))

        # Weigh the win/loss outcomes (-1 and 1) by their probabilities
        res = -1.0 * prob[classes.index('lost')] + 1.0 * prob[classes.index('won')]
        # print(res)

        return res

def maximizing(state):
    """
    Whether we're the maximizing player (1) or the minimizing player (2).
    :param state:
    :return:
    """
    return state.whose_turn() == 1


def features(state):
    # type: (State) -> tuple[float, ...]
    """
    Extract features from this state. Remember that every feature vector returned should have the same length.

    :param state: A state to be converted to a feature vector
    :return: A tuple of floats: a feature vector representing this state.
    """

    my_id = state.whose_turn()
    opponent_id = 1 if my_id == 2 else 2

    # # How many ships does p1 have in garrisons?
    # p1_garrisons = 0.0
    # # How many ships does p2 have in garrisons?
    # p2_garrisons = 0.0
    #
    # p1_planets = 0
    # p2_planets = 0
    #
    # for planet in state.planets(my_id):
    #     p1_garrisons += state.garrison(planet)
    #     p1_planets += 1
    #
    # for planet in state.planets(opponent_id):
    #     p2_garrisons += state.garrison(planet)
    #     p2_planets += 1
    #
    #
    # # How many ships does p1 have in fleets?
    # p1_fleets = 0.0
    # # How many ships does p2 have in fleets?
    # p2_fleets = 0.0
    #
    #
    # for fleet in state.fleets():
    #     if fleet.owner() == my_id:
    #         p1_fleets = fleet.size()
    #     else:
    #         p2_fleets += fleet.size()

    planets = {
        'owner': [],
        'garrisoned': [],
        'locationx': [],
        'locationy': [],
        'size': [],
        'turns_per_ship': []
    }

    fleets = {
        'owner': [],
        'size': [],
        'targetx': [],
        'targety': [],
        'distance': []
    }

    turninfo = {
        'current': state.turn_nr()
    }

    for planet in state.planets(my_id):
        planets['owner'].append(0)
        planets['garrisoned'].append(state.garrison(planet))
        planets['locationx'].append(planet.coords()[0])
        planets['locationy'].append(planet.coords()[1])
        planets['size'].append(planet.size())
        planets['turns_per_ship'].append(planet.turns_per_ship())

    for planet in state.planets(opponent_id):
        planets['owner'].append(1)
        planets['garrisoned'].append(state.garrison(planet))
        planets['locationx'].append(planet.coords()[0])
        planets['locationy'].append(planet.coords()[1])
        planets['size'].append(planet.size())
        planets['turns_per_ship'].append(planet.turns_per_ship())

    for planet in state.planets(0):
        planets['owner'].append(2)
        planets['garrisoned'].append(state.garrison(planet))
        planets['locationx'].append(planet.coords()[0])
        planets['locationy'].append(planet.coords()[1])
        planets['size'].append(planet.size())
        planets['turns_per_ship'].append(planet.turns_per_ship())

    for fleet in state.fleets():
        if fleet.owner() == my_id:
            fleets['owner'].append(0)
        else:
            fleets['owner'].append(1)
        target_planet = fleet.target();
        fleets['targetx'].append(target_planet.coords()[0])
        fleets['targety'].append(target_planet.coords()[1])
        fleets['size'].append(fleet.size())

        fleets['distance'].append(fleet.distance())

    while fleets['owner'].__len__() < 12:
        fleets['owner'].append(2)
        fleets['size'].append(0)
        fleets['targetx'].append(0)
        fleets['targety'].append(0)
        fleets['distance'].append(0)

    return planets['owner'][0], planets['owner'][1], planets['owner'][2], \
           planets['owner'][3], planets['owner'][4], planets['owner'][5], \
           planets['garrisoned'][0], planets['garrisoned'][1], planets['garrisoned'][2], \
           planets['garrisoned'][3], planets['garrisoned'][4], planets['garrisoned'][5], \
           planets['locationx'][0], planets['locationx'][1], planets['locationx'][2], \
           planets['locationx'][3], planets['locationx'][4], planets['locationx'][5], \
           planets['locationy'][0], planets['locationy'][1], planets['locationy'][2], \
           planets['locationy'][3], planets['locationy'][4], planets['locationy'][5], \
           planets['size'][0], planets['size'][1], planets['size'][2], \
           planets['size'][3], planets['size'][4], planets['size'][5], \
           planets['turns_per_ship'][0], planets['turns_per_ship'][1], planets['turns_per_ship'][2], \
           planets['turns_per_ship'][3], planets['turns_per_ship'][4], planets['turns_per_ship'][5], \
           fleets['owner'][0], fleets['owner'][1], fleets['owner'][2], \
           fleets['owner'][3], fleets['owner'][4], fleets['owner'][5], \
           fleets['owner'][6], fleets['owner'][7], fleets['owner'][8], \
           fleets['owner'][9], fleets['owner'][10], fleets['owner'][11], \
           fleets['size'][0], fleets['size'][1], fleets['size'][2], \
           fleets['size'][3], fleets['size'][4], fleets['size'][5], \
           fleets['size'][6], fleets['size'][7], fleets['size'][8], \
           fleets['size'][9], fleets['size'][10], fleets['size'][11], \
           fleets['targetx'][0], fleets['targetx'][1], fleets['targetx'][2], \
           fleets['targetx'][3], fleets['targetx'][4], fleets['targetx'][5], \
           fleets['targetx'][6], fleets['targetx'][7], fleets['targetx'][8], \
           fleets['targetx'][9], fleets['targetx'][10], fleets['targetx'][11], \
           fleets['targety'][0], fleets['targety'][1], fleets['targety'][2], \
           fleets['targety'][3], fleets['targety'][4], fleets['targety'][5], \
           fleets['targety'][6], fleets['targety'][7], fleets['targety'][8], \
           fleets['targety'][9], fleets['targety'][10], fleets['targety'][11], \
           fleets['distance'][0], fleets['distance'][1], fleets['distance'][2], \
           fleets['distance'][3], fleets['distance'][4], fleets['distance'][5], \
           fleets['distance'][6], fleets['distance'][7], fleets['distance'][8], \
           fleets['distance'][9], fleets['distance'][10], fleets['distance'][11], \
           turninfo['current']


# fleets['target'][0], fleets['target'][1], fleets['target'][2], \
# fleets['target'][3], fleets['target'][4], fleets['target'][5], \
# fleets['target'][6], fleets['target'][7], fleets['target'][8], \
# fleets['target'][9], fleets['target'][10], fleets['target'][11], \

