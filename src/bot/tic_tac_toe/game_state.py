from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

import discord
from discord import Embed

from src.conf import Conf


class Piece(Enum):
    EMPTY = ' '
    P1 = 'X'
    P2 = 'O'


class Turn(Enum):
    P1 = 'P1'
    P2 = 'P2'


class Board:
    def __init__(self):
        self.data: List[List[Piece]] = [[Piece.EMPTY] * 3 for _ in range(3)]

    def __iter__(self):
        return iter(self.data)

    def str_to_index_pair(self, pos: str) -> Tuple[int, int]:
        pos = pos.lower()
        if len(pos) != 2:
            raise Exception('Expected 2 character input for position')
        ind1 = ord(pos[0]) - ord('a')
        ind0 = ord(pos[1]) - ord('1')
        if ind0 < 0 or ind1 < 0 or ind0 >= len(self.data) or ind1 >= len(
                self.data[0]):
            raise Exception(
                f'Unable to find position for {pos}. Translated to {ind0}, '
                f'{ind1}')
        return ind0, ind1

    def __getitem__(self, pos: str) -> Piece:
        ind0, ind1 = self.str_to_index_pair(pos)
        return self.data[ind0][ind1]

    def __setitem__(self, pos: str, value: Piece):
        ind0, ind1 = self.str_to_index_pair(pos)
        assert self.data[ind0][ind1] == Piece.EMPTY
        self.data[ind0][ind1] = value


@dataclass
class GameState:
    p1: int
    p2: int
    board: Board = field(default_factory=Board)
    turn: Turn = Turn.P1

    @property
    def next_player_id(self) -> int:
        return self.p1 if self.turn == Turn.P1 else self.p2

    @property
    def curr_player_piece(self):
        return Piece.P1 if self.turn == Turn.P1 else Piece.P2

    def as_embed(self):
        h_line = '-' * 11 + '\n'
        result = '```\n'
        result += '  A | B | C\n'
        for i, row in enumerate(self.board, 1):
            result += h_line
            result += f'{i} {row[0].value} | {row[1].value} | {row[2].value}\n'
        result += '```'
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def move(self, player: discord.User, pos: str) -> str:
        if self.next_player_id != player.id:
            return f'It\'s not your turn. <@{self.next_player_id}> to play'
        try:
            piece_at_pos = self.board[pos]
        except Exception as e:
            return str(e)
        if piece_at_pos != Piece.EMPTY:
            return f'Position already occupied by {piece_at_pos.value}'
        self.board[pos] = self.curr_player_piece
        self.switch_turn()
        return f'It is now <@{self.next_player_id}> to play'

    def switch_turn(self):
        self.turn = Turn.P1 if self.turn == Turn.P2 else Turn.P2
