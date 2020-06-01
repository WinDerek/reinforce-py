import numpy as np
import random


def true_with_probability(prob):
    # Check legal input or not
    if prob < 0 or prob > 1:
        raise ValueError('The argument prob must be in range [0, 1], got {}'.format(prob))
    
    return random.random() < prob


def choose_randomly(distribution):
    """Selects a choice randomly according to the probability distribution of the choices.

    0.0------|--rand----|----|----1.0

    Arguments:
        distribution: {dict}. -- { choice : probability }.
    """

    rand = random.random()
    range_right = 0.0
    for choice, probability in distribution.items():
        range_right += probability
        if range_right > rand:
            return choice
