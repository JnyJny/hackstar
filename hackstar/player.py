"""
"""

from loguru import logger

import tcod as libtcod

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return '@'

    def draw(self, console=0):
        """
        """
        libtcod.console_put_char(console, self.x, self.y, str(self), libtcod.BKGND_NONE)

    def move(self, x, y):
        """
        """
        self.x += x
        self.y += y
