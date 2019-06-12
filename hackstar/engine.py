"""
"""

import tcod as libtcod
from pathlib import Path

from .player import Player

class TheGame:
    """
    """
    def __init__(self, w=80, h=50, font=None):
        self.w = w
        self.h = h
        self._resources = Path(__file__).resolve().parent / 'resources'
        self.font = self._resources / (font or 'arial10x10.png')
        libtcod.console_set_custom_font(str(self.font),
                                        libtcod.FONT_TYPE_GREYSCALE|libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(self.w, self.h, 'HackSt*r', False)
        self.console = 0
        self.player = Player(0,0)


    def run(self):
        """
        """
        while not libtcod.console_is_window_closed():
            self.update()
            self.draw()
            self.flush()
            self.dispatch(libtcod.console_check_for_keypress())

    def update(self):
        """
        """

    def draw(self):
        """
        """
        libtcod.console_set_default_foreground(self.console, libtcod.white)
        self.player.draw(self.console)
        

    def flush(self):
        """
        """
        libtcod.console_flush()

    def dispatch(self, key):

        if key.vk == libtcod.KEY_ESCAPE:
            quit()


