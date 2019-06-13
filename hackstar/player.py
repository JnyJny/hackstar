"""
"""

from loguru import logger

from .entity import Entity

import tcod


class Player(Entity):
    """
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, "@", tcod.green, "The Player")
