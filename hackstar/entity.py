"""
"""
from loguru import logger

import tcod

from dataclasses import dataclass, field
from enum import IntEnum


class Entities(IntEnum):
    INVALID = -1
    CORPSE = 0
    PLAYER = 1
    MONSTER = 2
    ITEM = 3


@dataclass
class Entity:
    x: int
    y: int
    onscreen: str
    fg: int
    health: int = 100
    kind: int = field(init=False)

    def __str__(self):
        return self.onscreen[0]

    @property
    def name(self) -> str:
        """Entity name.
        """
        try:
            return self._name
        except AttributeError:
            pass
        self._name = f"{self.__class__.__name__} {hex(id(self))}"
        return self._name

    @name.setter
    def name(self, new_name) -> None:
        self._name = new_name

    @property
    def position(self) -> tuple:
        """The coordinate tuple (x,y) for this entity.
        """
        return (self.x, self.y)

    @position.setter
    def position(self, new_position) -> None:
        """Set the entity's coordinates using a tuple or list.
        """
        self.x, self.y, = new_position[:2]

    @property
    def is_alive(self):
        """Returns True if this entity is alive."""
        try:
            return self.hp > 0
        except AttributeError:
            pass
        return False

    def move(self, dx: int, dy: int) -> None:
        """Moves the entity by dx and dy and returns the previous coordinates
        as an (x,y) tuple.

        :param int dx:
        :param int dy:
        :return: Tuple[int, int]
        """
        x, y = self.x, self.y
        self.x += dx
        self.y += dy
        self.last = (x, y)
        return (x, y)

    def move_towards(self, target_x: int, target_y: int, game_map) -> None:
        """
        """

        dx = target_x - self.x
        dy = target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        dx, dy = int(dx // distance), int(dy // distance)

        logger.info(
            f"Entity {self.name} wants to move toward {(target_x, target_y)} -> {(dx, dy)}"
        )

        x, y = self.x + dx, self.y + dy

        if game_map.is_blocked(x, y):
            logger.info(f"Entity {self.name} blocked at {(x, y)}")
            return False

        entity = game_map.entity_at((x, y))
        if entity and entity.is_monster and entity is not self:
            logger.info(f"Entity {self.name} blocked at {(x, y)} by {entity}")
            return False

        self.move(dx, dy)
        logger.info(f"Entity {self.name} did move toward {(target_x, target_y)}")
        return True

    def move_astar(self, target, game_map):
        """
        """

        logger.debug(f"{self.name} A* Observe")

        fov = tcod.map_new(game_map.w, game_map.h)

        for tile in game_map:
            tcod.map_set_properties(
                fov, tile.x, tile.y, not tile.opaque, not tile.blocked
            )

        for entity in game_map.entities:
            if entity == self:
                continue
            if entity.kind != Entities.ITEM:
                tcod.map_set_properties(fov, entity.x, entity.y, True, False)

        my_path = tcod.path_new_using_map(fov, 1.41)

        logger.debug(f"{self.name} A* Orient")
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        logger.debug(f"{self.name} A* Decide")
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            logger.debug("{self.name} A* Act 0")
            self.position = tcod.path_walk(my_path, True)
        else:
            logger.debug(f"{self.name} A* Act 1")
            self.move_towards(target.x, target.y, game_map)

        tcod.path_delete(my_path)

    def distance_to(self, other):
        """
        """
        try:
            dx, dy = other.x - self.x, other.y - self.y
        except AttributeError:
            dx, dy = other[0] - self.x, other[1] - self.y

        return (dx ** 2 + dy ** 2) ** 0.5

    def erase(self, console, blank: str = " ", bg: int = None) -> None:
        """Erase this entity at it's current coords.
        :param tcod.Console console:
        :param str blank:
        :param int x:
        :param int y:
        """
        bg = bg or tcod.BKGND_NONE
        tcod.console_put_char(console, self.x, self.y, blank, bg)

    def draw(self, console: int = 0, blank: bool = True) -> None:
        """Draw this entity at it's (x,y) coordinates on the specified console.
        :param int console:
        :param bool blank:
        """
        tcod.console_set_default_foreground(console, self.fg)
        tcod.console_put_char(console, self.x, self.y, str(self), tcod.BKGND_NONE)

    def move_and_draw(self, dx: int, dy: int, console: int = 0) -> None:
        """
        :param int dx:
        :param int dy:
        :param int console:

        """
        self.erase(console)
        self.x += dx
        self.y += dy
        self.draw(console)

    @property
    def is_player(self) -> bool:
        return self.kind == Entities.PLAYER

    @property
    def is_monster(self) -> bool:
        return self.kind == Entities.MONSTER

    @property
    def is_item(self) -> bool:
        return self.kind == Entities.ITEM

    @property
    def is_corpse(self) -> bool:
        return self.kind == Entities.CORPSE
