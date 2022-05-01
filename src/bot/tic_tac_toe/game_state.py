from dataclasses import dataclass, field
from enum import Enum
from typing import List

import discord
from discord import Embed

from src.conf import Conf


class Position(Enum):
    EMPTY = ' '
    X = 'X'
    O = 'O'


class Turn(Enum):
    P1 = 'P1'
    P2 = 'P2'


class Board:
    def __init__(self):
        self.data: List[List[Position]] = [[Position.EMPTY] * 3] * 3

    def __iter__(self):
        return iter(self.data)


@dataclass
class GameState:
    p1: int
    p2: int
    board: Board = field(default_factory=Board)
    turn: Turn = Turn.P1

    def as_embed(self):
        h_line = '-' * 11 + '\n'
        result = '```\n'
        result += '  A | B | C\n'
        for i, row in enumerate(self.board, 1):
            result += h_line
            result += f'{i} {row[0].value} | {row[1].value} | {row[2].value}\n'
        result += '```'
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def move(self, player: discord.User, pos: str):
        pass
