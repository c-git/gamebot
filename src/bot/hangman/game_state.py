from enum import Enum
from typing import Optional

from discord import Embed

from src.conf import Conf


class Guesser(Enum):
    P1 = 'P1'
    P2 = 'P2'


class GameState:
    def __init__(self, p1: int, p2: int):
        self.p1 = p1
        self.p2 = p2
        self.guesser: Guesser = Guesser.P2
        self.word: Optional[str] = None

    def as_embed(self):
        result = ''
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def user_input(self, player: int, inp: str):
        pass
