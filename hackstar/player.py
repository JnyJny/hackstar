"""
"""

import tcod
from loguru import logger
from .entity import Entity, Entities
from .components.fighter import Fighter


class Player(Entity, Fighter):
    """A player entity.
    """

    kind = Entities.PLAYER

    def kill(self):
        self.kind = Entities.CORPSE
        self.char = "%"
        self.color = tcod.dark_red
        return "You died!"
