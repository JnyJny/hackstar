"""
"""

from loguru import logger

import tcod


class Player:
    """
    """

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.o_x = x
        self.o_y = y

    def __str__(self) -> str:
        return "@"

    def draw(self, console: int = 0) -> None:
        """Draw the player on the screen.
        :param int console:
        """

        if (self.o_x, self.o_y) != (self.x, self.y):
            tcod.console_put_char(console, self.o_x, self.o_y, " ", tcod.BKGND_NONE)

        tcod.console_put_char(console, self.x, self.y, str(self), tcod.BKGND_NONE)

    def move(self, x: int, y: int) -> None:
        """Update the player's position.
        :param int x:
        :param int y:
        """
        self.o_x, self.o_y = self.x, self.y
        self.x += x
        self.y += y
