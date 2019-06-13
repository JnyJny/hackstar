"""map user input to actions
"""

from loguru import logger
import tcod


class BaseAction(Exception):
    pass


class MoveAction(BaseAction):
    def __init__(self, x, y):
        self.x, self.y = (x, y)


class FullscreenAction(BaseAction):
    pass


class QuitAction(BaseAction):
    pass


def action_exceptions(key, mouse) -> None:
    """
    :param tcod.Key key:
    :param tcod.Mouse mouse:

    :raises MoveAction:
    :raises FullscreenAction:
    :raises QuitAction:

    :return: None

    """

    if key.vk == tcod.KEY_NONE:
        return

    c = chr(key.c)

    if key.vk == tcod.KEY_UP or c == "i":
        raise MoveAction(0, -1)

    if c == "y":
        raise MoveAction(-1, -1)

    if c == "u":
        raise MoveAction(1, -1)

    if c == "b":
        raise MoveAction(-1, 1)

    if c == "n":
        raise MoveAction(1, 1)

    if key.vk == tcod.KEY_DOWN or c == "k":
        raise MoveAction(0, 1)

    if key.vk == tcod.KEY_LEFT or c == "j":
        raise MoveAction(-1, 0)

    if key.vk == tcod.KEY_RIGHT or c == "l":
        raise MoveAction(1, 0)

    if key.vk == tcod.KEY_ENTER and key.lalt:
        raise FullscreenAction()

    if key.vk == tcod.KEY_ESCAPE:
        raise QuitAction()
