"""
"""

from loguru import logger


class BasicMonster:
    """
    """

    def take_turn(self, target, game_map) -> None:
        """
        """
        if game_map.in_fov(self.x, self.y):
            logger.info(f"The {self.name} can see you!")
            if self.distance_to(target) >= 2:
                logger.info(f"I'm coming to gitcha {target.name}!")
                self.move_towards(target.x, target.y, game_map)
            elif target.hp > 0:
                logger.info(f"The {self.name} insults you! Your ego is damaged!")
        else:
            logger.info(f"The {self.name} sings a quiet ditty to itself.")
