"""here be.
"""

import tcod
import random

from loguru import logger
from .entity import Entity, Entities
from .components.fighter import Fighter
from .components.ai import BasicMonster


class Monster(Entity, Fighter, BasicMonster):
    """A monster entity.
    """

    kind = Entities.MONSTER

    def kill(self):
        msg = f"{self.name.capitalized()} is dead!"
        self.kind = Entities.CORPSE
        self.char = "%"
        self.color = tcod.dark_red
        self.blocks = False
        self.name = f"remains of {self.name}"
        return msg


class Troll(Monster):
    onscreen = "T"
    fg = tcod.darker_green


class Orc(Monster):
    onscreen = "o"
    fg = tcod.desaturated_green


class Goblin(Monster):
    onscreen = "g"
    fg = tcod.black


class Gnome(Monster):
    onscreen = "G"
    fg = tcod.orange


_monsters = [Troll, Orc, Goblin, Gnome]


def random_monster(x: int = 0, y: int = 0, level: int = 0):
    """
    """
    M = random.choice(_monsters)
    return M(x, y, M.onscreen, M.fg)
