"""
"""


class Tile:
    """
    """

    def __init__(self, x, y, blocked: bool, opaque: bool = None):
        self.x = x
        self.y = y
        self.blocked = blocked
        if opaque is None:
            opaque = blocked
        self.opaque = opaque

    @property
    def is_wall(self):
        return self.blocked and self.opaque

    @property
    def is_floor(self):
        return not self.blocked
