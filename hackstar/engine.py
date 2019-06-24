"""Game Event Loop
"""

import tcod
import random

from loguru import logger
from pathlib import Path

from .player import Player
from .monsters import random_monster
from .items import Item

from .actions import action_exceptions
from .actions import MoveAction
from .actions import IdleAction
from .actions import FullscreenAction
from .actions import QuitAction
from .actions import InventoryAction

from .maps import Map, Tile, Rect
from .states import GameState
from .util import random_xy


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

        self.font = self._resources / (font or "arial20x20.png")

        tcod.console_set_custom_font(
            str(self.font), tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
        )

        tcod.console_init_root(self.w, self.h, "HaCkStAr", fullscreen)
        self.console = tcod.console_new(self.w, self.h)

        logger.info(f"Console dimensions {w}x{h}")
        logger.info(f"Font: {self.font}")

        for i, entity in enumerate(self.map.entities):
            logger.info(f"Entity {i} {entity!r}")

        self.fov_algorithm = 0
        self.fov_light_walls = True
        self.fov_radius = 10

        self.player_turn_results = []
        self.monster_turn_results = []

        self.state = GameState.PLAYER_TURN

    @property
    def player(self):
        try:
            return self._player
        except AttributeError:
            pass
        self._player = Player(
            self.w // 2, self.h // 2, "@", tcod.black, tcod.BKGND_NONE
        )
        return self._player

    @property
    def colors(self):
        try:
            return self._colors
        except AttributeError:
            pass
        self._colors = {
            "dark_wall": tcod.Color(0, 0, 100),
            "dark_grnd": tcod.Color(50, 50, 150),
            "light_wall": tcod.Color(130, 110, 50),
            "light_grnd": tcod.Color(200, 180, 50),
        }
        return self._colors

    @property
    def map(self):
        try:
            return self._map
        except AttributeError:
            pass
        self._map = Map(self.w, self.map_h, self.player)
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

    def player_turn(self, action=None) -> None:
        """Handle the player's action
        :param action:
        """

        if self.state != GameState.PLAYER_TURN:
            return

        logger.info(f"Player Turn: action={action!r} {self.player!r} {self.player.hp}")

        self.state = GameState.MONSTER_TURN

        if isinstance(action, MoveAction):

            x, y = self.player.x + action.x, self.player.y + action.y

            entity = self.map.entity_at((x, y))

            if entity and entity.is_monster:
                self.player_turn_results.append(self.player.attack(entity))
            else:
                if entity:
                    logger.info(f"There is a {entity!r} here")

                if self.map.is_blocked(x, y):
                    logger.info(f"move to {(x,y)} obstructed.")
                else:
                    self.player.erase(self.console)
                    self.player.move(action.x, action.y)
                    self.map.needs_fov_recompute = True
            return

    def monsters_turn(self, action=None) -> None:
        """
        :param action:
        """

        logger.info(f"Monster Turn: action={action}")

        for entity in self.map.entities:
            try:
                entity.erase(self.console)
                self.monster_turn_results.append(
                    entity.take_turn(self.player, self.map)
                )
            except AttributeError:
                pass

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

        except IdleAction as action:
            self.state = GameState.MONSTER_TURN

        except MoveAction as action:

            self.player_turn(action)

        except FullscreenAction:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        except QuitAction:
            logger.debug("Quit")
            exit(0)

        except Exception as unknown_action:
            logger.debug(f"Caught unknown action {unknown_action}")

        for player_turn_result in self.player_turn_results:
            message = player_turn_result.get("msg")
            deader = player_turn_result.get("dead")

            if message:
                logger.info(message)

            if deader and not deader.is_alive:
                message = deader.kill()
                if deader is self.player:
                    self.state = GameState.PLAYER_DEAD
                logger.info(message)
                logger.debug(
                    f"{deader.name.capitalize()} is DEAD! <{deader.hp}> {not deader.is_alive}"
                )

        self.player_turn_results.clear()

        if self.state == GameState.MONSTER_TURN:

            self.monsters_turn()

            for monster_turn_result in self.monster_turn_results:
                message = monster_turn_result.get("msg")
                deader = monster_turn_result.get("dead")

                if message:
                    logger.info(message)

                if deader:
                    message = deader.kill()
                    logger.info(message)
                    logger.debug(
                        f"{deader.name.capitalize()} is DEAD! <{deader.hp}> {not deader.is_alive}"
                    )

                    if deader is self.player:
                        self.state = GameState.PLAYER_DEAD
                        break
            else:
                self.state = GameState.PLAYER_TURN

            self.monster_turn_results.clear()

        # XXX the player object should hold FOV radius, light walls
        #     since those are related to the player ( and map has a
        #     reference to player ).

        self.map.update(self.fov_radius, self.fov_light_walls, self.fov_algorithm)

    def draw(self) -> None:
        """Draw game state to screen.
        """

        tcod.console_set_default_foreground(self.console, tcod.white)

        self.map.draw(self.console, self.colors)

        tcod.console_blit(self.console, 0, 0, self.w, self.h, 0, 0, 0)

    def flush(self) -> None:
        """Push drawn state to screen.
        """
        tcod.console_flush()
