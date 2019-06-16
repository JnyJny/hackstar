"""
"""
from loguru import logger
import tcod

from dataclasses import dataclass, field
from enum import IntEnum


class Entities(IntEnum):
    INVALID = -1
    PLAYER = 0
    MONSTER = 1
    ITEM = 2


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
        self._name = self.__class__.__name__
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @property
    def position(self) -> tuple:
        """The coordinate tuple (x,y) for this entity.
        """
        return (self.x, self.y)

    @position.setter
    def position(self, new_position):
        """Set the entity's coordinates using a tuple or list.
        """
        self.x, self.y, = new_position[:2]

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
        return (x, y)

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

    def attack(self, other):
        """Attack the other entity.
        """
        logger.info(f"{self.name} is attacking {other.name}")
