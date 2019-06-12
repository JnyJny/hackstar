"""
"""

from loguru import logger
import tcod as libtcod
from pathlib import Path

from .player import Player
from .actions import (action_exceptions,
                      MoveAction,
                      FullscreenAction,
                      QuitAction)

class TheGame:
    """You Lost.
    """
    
    def __init__(self, w=80, h=50, font=None, fullscreen=False):
        """
        """
        
        self.w = w
        self.h = h
        self._resources = Path(__file__).resolve().parent / 'resources'
        self.font = self._resources / (font or 'arial10x10.png')
        self.fullscreen = fullscreen

        logger.info(f'Console dimensions {w}x{h}')
        logger.info(f'Font: {self.font}')
        
        libtcod.console_set_custom_font(str(self.font),
                                        libtcod.FONT_TYPE_GREYSCALE|libtcod.FONT_LAYOUT_TCOD)
        libtcod.console_init_root(self.w, self.h, 'HaCkStAr', self.fullscreen)
        self.console = 0
        self.player = Player(self.w//2, self.h//2)

    @property
    def key(self):
        """Key is a tcod.Key object.
        """
        try:
            return self._key
        except AttributeError:
            pass
        self._key = libtcod.Key()
        return self._key

    @property
    def mouse(self):
        """Mouse is a tcod.Mouse object.
        """
        try:
            return self._mouse
        except AttributeError:
            pass
        self._mouse = libtcod.Mouse()
        return self._mouse


    def run(self):
        """Start the game loop.
        """
        while not libtcod.console_is_window_closed():
            self.update()
            self.draw()
            self.flush()

            
    def update(self):
        """Update game state.
        """            

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS,
                                    self.key,
                                    self.mouse)

        try:
            action_exceptions(self.key, self.mouse)
        except MoveAction as move:
            logger.debug(f'move action: {move}')
            self.player.move(move.x, move.y)
        except FullscreenAction:
            logger.debug('Fullscreen')
        except QuitAction:
            logger.debug('Quit')
            exit(0)



    def draw(self):
        """Draw game state to screen.
        """
        libtcod.console_set_default_foreground(self.console, libtcod.white)
        self.player.draw(self.console)
        

    def flush(self):
        """Push drawn state to screen.
        """
        libtcod.console_flush()

        

        

