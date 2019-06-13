"""
"""
from loguru import logger
import tcod

from dataclasses import dataclass


@dataclass
class Entity:
    x: int
    y: int
    onscreen: str
    color: int

    def __str__(self):
        return self.onscreen[0]

    def move(self, dx: int, dy: int) -> None:
        """
        :param int dx:
        :param int dy:
        :return: Tuple[int, int]
        """
        x, y = self.x, self.y
        self.x += dx
        self.y += dy
        return (x, y)

    def erase(self, console: int = 0, blank=" "):
        """
        """

        tcod.console_put_char(console, self.x, self.y, blank, tcod.BKGND_NONE)

    def draw(self, console: int = 0, blank=True):
        """Draw this entity at it's (x,y) coordinates on the specified console.
        """
        #        logger.debug(f"Drawing {str(self)} with {self.color}")
        tcod.console_set_default_foreground(console, self.color)
        tcod.console_put_char(console, self.x, self.y, str(self), tcod.BKGND_NONE)

    def move_and_draw(self, dx: int, dy: int, console: int = 0):

        self.erase(console)
        self.x += dx
        self.y += dy
        self.draw(console)
