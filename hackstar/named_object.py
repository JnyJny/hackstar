"""
"""

from dataclasses import dataclass

@dataclass
class NamedObject:
    name: str = "generic object"
    long: str = "an extraordinarily generic object"
    desc: str = "An extraordinarily generic object forged in the depths of memory from ancient electrons forged in the fires of the Big Bang"
