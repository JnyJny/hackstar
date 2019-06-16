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
from .actions import FullscreenAction
from .actions import QuitAction
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

        self.player = Player(self.w // 2, self.h // 2, "@", tcod.black, tcod.BKGND_NONE)

        self.add_entity(self.player)

        logger.info(f"Console dimensions {w}x{h}")
        logger.info(f"Font: {self.font}")

        for i, pair in enumerate(self.entities.items()):
            logger.info(f"Entity {i} @ {pair[0]}:  {pair[1]!r}")

        self.fov_algorithm = 0
        self.fov_light_walls = True
        self.fov_radius = 10

        self.state = GameState.PLAYER_TURN

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
        self._map = Map(self.w, self.map_h)
        self._map.dig_dungeon(self.player)
        for room in self._map.rooms:
            self.place_monsters(room, 3)
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

    @property
    def entities(self):
        try:
            return self._entities
        except AttributeError:
            pass
        self._entities = {}
        return self._entities

    def add_entity(self, entity):
        """
        :param .Entity subclass entity:
        :return: bool
        """
        stored = self.entities.setdefault(entity.position, entity)
        return stored == entity

    def entity_at(self, coords):
        """
        :param tuple coords:
        :return .Entity subclass:
        """
        return self.entities.get(coords, None)

    def remove_entity(self, entity):
        """
        :param .Entity subclass entity:
        :return: bool
        """

        try:
            position = entity.position
        except AttributeError:
            position = entity

        try:
            return self.entities.pop(position)
        except KeyError:
            pass
        logger.debug(f"Remove failed, no entity @ {position}")
        return None

    def place_monsters(self, room, max_monsters: int) -> list:
        """
        :param .maps.Rect room:
        :param int max_monsters:
        :return: list of monsters placed
        """
        n_monsters = random.randint(0, max_monsters)

        x_range = (room.x + 1, room.x1 - 1)
        y_range = (room.y + 1, room.y1 - 1)

        monsters = [random_monster() for _ in range(n_monsters)]

        for monster in monsters:
            logger.debug(f"Monster: {monster!r}")

        for monster in monsters:
            monster.position = random_xy(x_range, y_range)
            while not self.add_entity(monster):
                logger.debug(f"OCCUPADO @ {monster.position}")
                monster.position = random_xy(x_range, y_range)
            logger.debug(f"Placed monster {monster!r}")
        return monsters

    def player_turn(self, action=None):
        """
        """
        logger.info(f"Player Turn: action={action}")

        if isinstance(action, MoveAction):
            move = action
            x, y = self.player.x + move.x, self.player.y + move.y

            entity = self.entity_at((x, y))

            if entity and entity.is_monster:
                self.player.attack(entity)
            else:
                if entity:
                    logger.info(f"There is a {entity!r} here")

                if self.map.is_blocked(x, y):
                    logger.info(f"move to {(x,y)} obstructed.")
                else:
                    self.player.erase(self.console)
                    self.player.move(move.x, move.y)
                    self.map.needs_fov_recompute = True

        self.state = GameState.MONSTER_TURN

    def monsters_turn(self, action=None):

        logger.info(f"Monster Turn: action={action}")

        for coord, entity in self.entities.items():
            logger.info(f"Monster {entity.name} @ {coord} ponders the meaning of life")

        self.state = GameState.PLAYER_TURN

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

            if self.state == GameState.PLAYER_TURN:
                self.player_turn(move)

        except FullscreenAction:
            logger.debug("Fullscreen")
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        except QuitAction:
            logger.debug("Quit")
            exit(0)

        if self.state == GameState.MONSTER_TURN:
            self.monsters_turn()

        # XXX this should be moved into map.draw
        #     map needs a FOV radius, light_walls and algorithm

        self.map.recompute_fov(
            self.player.x,
            self.player.y,
            self.fov_radius,
            self.fov_light_walls,
            self.fov_algorithm,
        )

    def draw(self) -> None:
        """Draw game state to screen.
        """

        tcod.console_set_default_foreground(self.console, tcod.white)

        self.map.draw(self.console, self.colors)

        for coord, entity in self.entities.items():
            entity.draw(self.console)

        tcod.console_blit(self.console, 0, 0, self.w, self.h, 0, 0, 0)

    def flush(self) -> None:
        """Push drawn state to screen.
        """
        tcod.console_flush()
