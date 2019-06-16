"""
"""

from loguru import logger
from .entity import Entity, Entities


class Item(Entity):
    """An item entity.
    """

    kind = Entities.ITEM
