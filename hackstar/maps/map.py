"""
"""

import tcod
import random
from loguru import logger

from .tile import Tile
from .rect import Rect
from ..util import random_xy
from ..monsters import random_monster

# from ..items import random_item


class Map:
    def __init__(self, width, height, player) -> None:
        self.w = width
        self.h = height
        self.player = player
        self.needs_fov_recompute = True
        self.dig_dungeon()
        self.add_monsters()

    @property
    def tiles(self):
        try:
            return self._tiles
        except AttributeError:
            pass
        self._tiles = [[Tile(x, y, True) for y in range(self.h)] for x in range(self.w)]
        return self._tiles

    @property
    def rooms(self) -> list:
        """List of rooms managed by the map. Left over from dig_dungeons.
        """
        try:
            return self._rooms
        except AttributeError:
            pass
        self._rooms = []
        return self._rooms

    @property
    def entities(self) -> list:
        """List of entities in the map.
        """
        try:
            return self._entities
        except AttributeError:
            pass
        self._entities = []
        return self._entities

    def entity_at(self, coords):
        """Searches the entities list for an etity at the given
        coordinates in the map. The first matching entity is
        returned, otherwise None is returned for no matches.

        :param Tuple[int,int] coords:
        :return .Entity subclass:
        """
        for entity in self.entities:
            if entity.position == coords:
                return entity
        return None

    def populate_room(self, room, max_monsters: int) -> list:
        """Adds a random number of monsters up to max_monsters
        to the supplied room.


        :param .maps.Rect room:
        :param int max_monsters:
        :return: list of monsters placed
        """
        n_monsters = random.randint(0, max_monsters)

        # check that the n_monsters <= number of tiles in room

        x_range = (room.x + 1, room.x1 - 1)
        y_range = (room.y + 1, room.y1 - 1)

        monsters = [random_monster() for _ in range(n_monsters)]

        for monster in monsters:
            logger.debug(f"Monster: {monster!r}")

        for monster in monsters:
            monster.position = random_xy(x_range, y_range)
            while self.entity_at(monster.position):
                logger.debug(f"OCCUPADO @ {monster.position}")
                monster.position = random_xy(x_range, y_range)
            self.entities.append(monster)
            logger.debug(f"Placed monster {monster!r}")
        return monsters

    def add_monsters(self, max_monsters_per_room=3) -> None:
        """
        """
        logger.info("Adding monsters to rooms")
        for room in self.rooms:
            self.populate_room(room, max_monsters_per_room)

    def add_loot(self, max_loot_per_room=2) -> None:
        """
        """
        logger.info("Adding loot to rooms")

    def dig_dungeon(self, max_rooms=11, min_size=6, max_size=10):
        """
        """
        min_x, max_x = 0, self.w - 1
        min_y, max_y = 0, self.h - 1

        for _ in range(max_rooms):

            room = Rect.random(min_size, max_size, min_x, max_x, min_y, max_y)

            for other_room in self.rooms:
                if room in other_room:
                    break
            else:
                logger.debug(f"Room: {room}")
                self.dig_room(room)
                if len(self.rooms) == 0:
                    self.player.position = room.center
                    self.entities.append(self.player)
                    assert len(self.entities) == 1
                else:
                    room_x, room_y = room.center
                    other_x, other_y = self.rooms[-1].center
                    if random.randint(0, 1) == 1:
                        self.dig_h_hall(other_x, room_x, other_y)
                        self.dig_v_hall(other_y, room_y, room_x)
                    else:
                        self.dig_v_hall(other_y, room_y, other_x)
                        self.dig_h_hall(other_x, room_x, room_y)
                self.rooms.append(room)

    def dig_room(self, room) -> None:
        """
        """
        for x in room.xrange():
            for y in room.yrange():
                try:
                    tile = self.tiles[x][y]
                    tile.blocked = False
                    tile.opaque = False
                except IndexError as err:
                    logger.debug(f"{err} x={x} y={y}")

    def dig_h_hall(self, x0, x1, y):
        """
        """
        for x in range(min(x0, x1), max(x0, x1) + 1):
            t = self.tiles[x][y]
            t.blocked = False
            t.opaque = False

    def dig_v_hall(self, y0, y1, x):
        """
        """
        for y in range(min(y0, y1), max(y0, y1) + 1):
            t = self.tiles[x][y]
            t.blocked = False
            t.opaque = False

    def random_rooms(self, count=4):
        """
        """

        for _ in range(count):
            x = random.randint(1, self.w - 2)
            y = random.randint(1, self.h - 2)
            w = random.randint(4, 10)
            h = random.randint(4, 10)
            room = Rect(x, y, w, h)
            self.dig_room(room)

    def is_blocked(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].blocked

    def is_opaque(self, x: int, y: int) -> bool:
        """
        """
        return self.tiles[x][y].opaque

    def __iter__(self):
        self._x = 0
        self._y = 0
        return self

    def __next__(self):
        tile = self.tiles[self._x][self._y]
        self._x += 1

        if self._x >= self.w:
            self._x = 0
            self._y += 1

        if self._y >= self.h:
            raise StopIteration()

        return tile

    @property
    def fov_map(self):
        """tcod.Map
        """
        try:
            return self._fov_map
        except AttributeError:
            pass

        self._fov_map = tcod.map_new(self.w, self.h)

        for tile in self:
            tcod.map_set_properties(
                self._fov_map, tile.x, tile.y, not tile.opaque, not tile.blocked
            )
        return self._fov_map

    def in_fov(self, x: int, y: int) -> bool:
        """
        """
        return tcod.map_is_in_fov(self.fov_map, x, y)

    def update(self, radius, light_walls=True, algorithm=0) -> None:
        """
        """

        if self.needs_fov_recompute:
            logger.debug(
                f"Recomputing FOV for {self.player.position} radius {radius} algorithm:{algorithm}"
            )
            tcod.map_compute_fov(
                self.fov_map,
                self.player.x,
                self.player.y,
                radius,
                light_walls,
                algorithm,
            )

    def draw(self, console: int, colors: dict, force: bool = False) -> None:
        """
        """

        if self.needs_fov_recompute or force:
            for tile in self:
                visible = tcod.map_is_in_fov(self.fov_map, tile.x, tile.y)
                # XXX tile should take more responsibility for what it's color
                #     is depending on it's configuration.
                #
                color = 0x000000
                if tile.is_wall:
                    color = colors["light_wall"] if visible else colors["dark_wall"]
                if tile.is_floor:
                    color = colors["light_grnd"] if visible else colors["dark_grnd"]
                tcod.console_set_char_background(
                    console, tile.x, tile.y, color, tcod.BKGND_SET
                )
            self.needs_fov_recompute = False

        for entity in self.entities:
            entity.draw(console)
