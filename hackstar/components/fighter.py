"""
"""

from loguru import logger


class Fighter:
    """
    """

    def __init__(self, hp, defense, power):
        self.max_hp = hp
        self.hp = hp
        self.defense = defense
        self.power = power

    def attack(self, other):
        """Attack the other entity.
        """
        logger.info(f"{self.name} is attacking {other.name}")
