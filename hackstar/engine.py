"""Game Event Loop
"""

import tcod

from loguru import logger
from pathlib import Path

from .entity import Entity
from .player import Player
from .actions import action_exceptions
from .actions import MoveAction
from .actions import FullscreenAction
from .actions import QuitAction
from .maps import Map, Tile


class TheGame:
    """You Lost.
    """

    def __init__(
        self, w: int = 80, h: int = 50, font: str = None, fullscreen: bool = False
    ) -> None:
        """
        """

        self.w = w
        self.h = h
        self.map_h = self.h - 5

        self._resources = Path(__file__).resolve().parent / "resources"
        self.font = self._resources / (font or "arial10x10.png")

        logger.info(f"Console dimensions {w}x{h}")
        logger.info(f"Font: {self.font}")

        tcod.console_set_custom_font(
            str(self.font), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
        )

        tcod.console_init_root(self.w, self.h, "HaCkStAr", fullscreen)
        self.console = tcod.console_new(self.w, self.h)

        self.player = Entity(self.w // 2, self.h // 2, "@", tcod.green)
        self.npc = Entity(self.w // 2 + 4, self.h // 2, "@", tcod.red)

        self.entities = [self.player, self.npc]

    @property
    def colors(self):
        try:
            return self._colors
        except AttributeError:
            pass
        self._colors = {
            "dark_wall": tcod.Color(0, 0, 100),
            "dark_grnd": tcod.Color(50, 50, 150),
        }
        return self._colors

    @property
    def map(self):
        try:
            return self._map
        except AttributeError:
            pass
        self._map = Map(self.w, self.map_h)
        return self._map

    @property
    def key(self) -> tcod.Key:
        """Key is a tcod.Key object.
        """
        try:
            return self._key
        except AttributeError:
            pass
        self._key = tcod.Key()
        return self._key

    @property
    def mouse(self) -> tcod.Mouse:
        """Mouse is a tcod.Mouse object.
        """
        try:
            return self._mouse
        except AttributeError:
            pass
        self._mouse = tcod.Mouse()
        return self._mouse

    def run(self) -> None:
        """Start the game loop.
        """

        self.map.random_walls()

        while not tcod.console_is_window_closed():
            self.update()
            self.draw()
            self.flush()

    def update(self) -> None:
        """Update game state.
        """

        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS, self.key, self.mouse)

        try:
            action_exceptions(self.key, self.mouse)

        except MoveAction as move:
            logger.debug(f"move action: {move}")
            self.player.move_and_draw(move.x, move.y, self.console)

        except FullscreenAction:
            logger.debug("Fullscreen")
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        except QuitAction:
            logger.debug("Quit")
            exit(0)

    def draw(self) -> None:
        """Draw game state to screen.
        """

        tcod.console_set_default_foreground(self.console, tcod.white)

        self.map.draw(self.console, self.colors)

        for entity in self.entities:
            entity.draw(self.console)

        tcod.console_blit(self.console, 0, 0, self.w, self.h, 0, 0, 0)

    def flush(self) -> None:
        """Push drawn state to screen.
        """
        tcod.console_flush()
