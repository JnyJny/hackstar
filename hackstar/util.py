"""
"""

import random


def random_xy(x_range: tuple, y_range: tuple) -> tuple:
    """
    :param tuple x_range:
    :param tuple y_range:
    :return: Tuple[Int, Int]
    """

    return random.randint(*x_range), random.randint(*y_range)
