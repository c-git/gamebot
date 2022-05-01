from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

import discord
from discord import Embed

from src.conf import Conf


class Piece(Enum):
    EMPTY = ' '
    P1 = 'x'
    P2 = 'o'
    P1_WIN = 'X'
    P2_WIN = 'O'


class Turn(Enum):
    P1 = 'P1'
    P2 = 'P2'


def change_to_won_piece(piece: Piece):
    assert piece != Piece.EMPTY
    if piece == Piece.P1:
        return Piece.P1_WIN
    elif piece == Piece.P2:
        return Piece.P2_WIN
    else:
        assert piece == Piece.P1_WIN or piece == Piece.P2_WIN
        return piece


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

    def is_won(self) -> bool:
        """
        Checks if game is won AND changes winning pieces to the winning symbol
        ASSUMPTION: Board is square
        WARNING: Changes board to set pieces in win to new symbol
        NOTE: Function is idempotent
        :return: True if game has been won and false otherwise
        """
        # TODO Use position played to make more efficient implementation
        assert len(self.data) == len(self.data[0])
        n = len(self.data)
        # Check win by row
        for row in self.data:
            first_piece = row[0]
            if first_piece == Piece.EMPTY:
                break  # Cannot win if first piece is empty
            won = True
            for i in range(1, n):
                won = won and first_piece == row[i]
                if not won:
                    break
            if won:
                for i in range(n):
                    row[i] = change_to_won_piece(row[i])
                return True

        # Check win by column
        for col_ind in range(n):
            first_piece = self.data[0][col_ind]
            if first_piece == Piece.EMPTY:
                break  # Cannot win if first piece is empty
            won = True
            for row_ind in range(1, n):
                won = won and first_piece == self.data[row_ind][col_ind]
                if not won:
                    break
            if won:
                for row_ind in range(n):
                    self.data[row_ind][col_ind] = change_to_won_piece(
                        self.data[row_ind][col_ind])
                return True

        # Check win backward diagonal
        first_piece = self.data[0][0]
        won = first_piece != Piece.EMPTY
        for ind in range(1, n):
            won = won and first_piece == self.data[ind][ind]
            if not won:
                break
        if won:
            for ind in range(n):
                self.data[ind][ind] = change_to_won_piece(self.data[ind][ind])
            return True

        # Check win forward diagonal
        first_piece = self.data[- 1][- 1]
        won = first_piece != Piece.EMPTY
        for ind in range(2, n + 1):
            won = won and first_piece == self.data[-ind][-ind]
            if not won:
                break
        if won:
            for ind in range(1, n + 1):
                self.data[-ind][-ind] = change_to_won_piece(
                    self.data[-ind][-ind])
            return True

        return False

    def is_full(self) -> bool:
        for row in self.data:
            for position in row:
                if position == Piece.EMPTY:
                    return False
        return True


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
        if self.board.is_won():
            return f'WINNER!!! - <@{self.next_player_id}>'
        self.switch_turn()
        if self.board.is_full():  # Check for Draw
            return 'DRAW - Board full'
        return f'It is now <@{self.next_player_id}> to play'

    def switch_turn(self):
        self.turn = Turn.P1 if self.turn == Turn.P2 else Turn.P2
