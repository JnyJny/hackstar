"""map user input to actions
"""

from loguru import logger
import tcod


class BaseAction(Exception):
    pass


class MoveAction(BaseAction):
    def __init__(self, x, y):
        self.x, self.y = (x, y)


class IdleAction(BaseAction):
    pass


class InventoryAction(BaseAction):
    pass


class FullscreenAction(BaseAction):
    pass


class QuitAction(BaseAction):
    pass


_c_dispatch = {
    "h": MoveAction(-1, 0),
    "j": MoveAction(0, 1),
    "k": MoveAction(0, -1),
    "l": MoveAction(1, 0),
    "y": MoveAction(-1, -1),
    "u": MoveAction(1, -1),
    "b": MoveAction(-1, 1),
    "n": MoveAction(1, 1),
    ".": IdleAction(),
    "i": InventoryAction(),
}


_vk_dispatch = {
    tcod.KEY_UP: MoveAction(0, -1),
    tcod.KEY_DOWN: MoveAction(0, 1),
    tcod.KEY_LEFT: MoveAction(-1, 0),
    tcod.KEY_RIGHT: MoveAction(1, 0),
    tcod.KEY_ESCAPE: QuitAction(),
}


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

    try:
        action = _c_dispatch[c]
        raise action
    except KeyError:
        pass

    try:
        action = _vk_dispatch[key.vk]
        raise action
    except KeyError:
        pass

    if key.vk == tcod.KEY_ENTER and key.lalt:
        raise FullscreenAction()
