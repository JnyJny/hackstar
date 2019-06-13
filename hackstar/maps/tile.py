"""
"""


class Tile:
    """
    """

    def __init__(self, blocked: bool, block_sight: bool = None):
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight

    @property
    def is_wall(self):
        return self.blocked and self.block_sight

    @property
    def is_lava(self):
        return self.blocked and not self.block_sight

    @property
    def is_floor(self):
        return not self.blocked

    @property
    def is_dark(self):
        return self.block_sight
