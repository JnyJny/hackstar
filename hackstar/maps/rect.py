"""
"""

from dataclasses import dataclass
import random


@dataclass
class Rect:
    x: int
    y: int
    w: int
    h: int

    @classmethod
    def random(cls, min_size, max_size, min_x, max_x, min_y, max_y):
        """
        """
        w = random.randint(min_size, max_size)
        h = random.randint(min_size, max_size)
        x = random.randint(min_x, max_x - w)
        y = random.randint(min_y, max_y - h)
        return cls(x, y, w, h)

    def __post_init__(self):
        self.x1 = self.x + self.w
        self.y1 = self.y + self.h

    def __str__(self):
        return ",".join([str(p) for p in self.points])

    @property
    def points(self):
        """
        """
        p0 = self.x, self.y
        p1 = self.x, self.y1
        p2 = self.x1, self.y1
        p3 = self.x1, self.y
        return [p0, p1, p2, p3]

    @property
    def center(self):
        x = (self.x + self.x1) // 2
        y = (self.y + self.y1) // 2
        return (x, y)

    def xrange(self, step=1):
        """
        """
        return range(self.x + 1, self.x1, step)

    def yrange(self, step=1):
        """
        """
        return range(self.y + 1, self.y1, step)

    def __contains__(self, other):

        return (
            self.x <= other.x1
            and self.x1 >= other.x
            and self.y <= other.y1
            and self.y1 >= other.y
        )

    def has_point(self, point):
        """
        """
        x, y, *_ = point

        # XXX point in rect
