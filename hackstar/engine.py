"""Game Event Loop
"""

from loguru import logger
import tcod
from pathlib import Path

from .player import Player
from .actions import action_exceptions, MoveAction, FullscreenAction, QuitAction


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
        self._resources = Path(__file__).resolve().parent / "resources"
        self.font = self._resources / (font or "arial10x10.png")

        logger.info(f"Console dimensions {w}x{h}")
        logger.info(f"Font: {self.font}")

        tcod.console_set_custom_font(
            str(self.font), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
        )
        tcod.console_init_root(self.w, self.h, "HaCkStAr", fullscreen)
        self.console = 0
        self.player = Player(self.w // 2, self.h // 2)

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
            self.player.move(move.x, move.y)

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
        self.player.draw(self.console)
        tcod.console_blit(self.console, 0, 0, self.w, self.h, 0, 0, 0)

    def flush(self) -> None:
        """Push drawn state to screen.
        """
        tcod.console_flush()
