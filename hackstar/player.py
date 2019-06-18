"""
"""

from loguru import logger
from .entity import Entity, Entities
from .components.fighter import Fighter


class Player(Entity, Fighter):
    """A player entity.
    """

    kind = Entities.PLAYER
