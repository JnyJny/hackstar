"""
"""

from loguru import logger
from dataclasses import dataclass


class Fighter:
    """
    """

    @property
    def max_hp(self) -> int:
        return 3

    @property
    def hp(self) -> int:
        try:
            return self._hp
        except AttributeError:
            pass
        self._hp = self.max_hp
        return self._hp

    @hp.setter
    def hp(self, new_value) -> None:
        self._hp = new_value

    @property
    def defense(self) -> int:
        try:
            return self._defense
        except AttributeError:
            pass
        self._defense = 0
        return self._defense

    @defense.setter
    def defense(self, new_value) -> None:
        self._defense = new_value

    @property
    def power(self) -> int:
        try:
            return self._power
        except AttributeError:
            pass
        self._power = 1
        return self._power

    def attack(self, target) -> dict:
        """Attack the other entity.
        """
        damage = self.power - target.defense

        result = {"src": self, "dst": target, "msg": ""}

        if damage > 0:
            target.take_damage(damage)
            message = (
                f"{self.name} attacks {target.name} for {damage} damage! {target.hp}"
            )
            logger.info(message)
        else:
            message = f"{self.name} attacks {target.name} and missses!"
            logger.info(message)

        result["msg"] = message

        return result

    def take_damage(self, amount) -> None:
        """
        """
        self.hp -= amount
