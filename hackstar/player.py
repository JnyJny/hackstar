"""
"""

from loguru import logger
from .entity import Entity, Entities


class Player(Entity):
    """A player entity.
    """

    kind = Entities.PLAYER
