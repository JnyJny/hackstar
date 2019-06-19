"""
"""

from loguru import logger
from dataclasses import dataclass


class Fighter:
    """
    """

    @property
    def max_hp(self):
        return 100

    @property
    def hp(self):
        try:
            return self._hp
        except AttributeError:
            pass
        self._hp = self.max_hp
        return self._hp

    @hp.setter
    def hp(self, new_value):
        self._hp = max(self._hp + new_value, self.max_hp)

    @property
    def defense(self):
        try:
            return self._defense
        except AttributeError:
            pass
        self._defense = 0
        return self._defense

    @defense.setter
    def defense(self, new_value):
        self._defense = new_value

    @property
    def power(self):
        try:
            return self._power
        except AttributeError:
            pass
        self._power = 1
        return self._power

    def attack(self, other):
        """Attack the other entity.
        """
        logger.info(f"{self.name} is attacking {other.name}")
