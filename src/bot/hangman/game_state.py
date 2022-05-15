from dataclasses import dataclass
from enum import Enum

import discord
from discord import Embed

from src.conf import Conf


class Guesser(Enum):
    P1 = 'P1'
    P2 = 'P2'


@dataclass
class GameState:
    p1: int
    p2: int
    guesser: Guesser = Guesser.P2

    def as_embed(self):
        result = ''
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def user_input(self, player: discord.User, inp: str):
        pass
