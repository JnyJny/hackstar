from enum import IntEnum


class GameState(IntEnum):
    PLAYER_TURN = 1
    MONSTER_TURN = 2
    PLAYER_DEAD = 3
