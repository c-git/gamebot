from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Position(Enum):
    EMPTY = 'EMPTY'
    X = 'X'
    O = 'O'


class Turn(Enum):
    P1 = 'P1'
    P2 = 'P2'


class Board:
    def __init__(self):
        self.data: List[List[Position]] = [[Position.EMPTY] * 3] * 3


@dataclass
class GameState:
    p1: int
    p2: int
    board: Board = field(default_factory=Board)
    turn: Turn = Turn.P1
