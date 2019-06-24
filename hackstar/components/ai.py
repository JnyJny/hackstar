"""
"""

from loguru import logger


class BasicMonster:
    """
    """

    def take_turn(self, target, game_map) -> dict:
        """
        """

        logger.debug(f"{self.name} is fixin' to take his/her/it's turn.")

        result = {"src": self, "dst": target, "msg": ""}

        if not self.is_alive:
            logger.debug(f"{self.name} seems to be dead: {self.hp} {self.is_alive}")
            result["msg"] = "Dead things can't take a turn."
            return result

        if game_map.in_fov(self.x, self.y):
            message = f"The {self.name} can see the {target.name.capitalize()}!"
            logger.info(message)
            if self.distance_to(target) >= 2:
                message = f'The {self.name} says "I\'m coming to gitcha {target.name}!"'
                logger.info(message)
                self.move_astar(target, game_map)
            elif target.hp > 0:
                message = self.attack(target)
        else:
            message = f"The {self.name.capitalize()} sings a quiet ditty to itself and dreams of mayhem."
            logger.info(message)

        result["msg"] = message

        return result
