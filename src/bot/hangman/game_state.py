from enum import Enum
from typing import List, Optional, Set

from discord import Embed

from src.conf import Conf


class Guesser(Enum):
    P1 = 'P1'
    P2 = 'P2'


class GameState:
    def __init__(self, p1: int, p2: int):
        self.p1 = p1
        self.p2 = p2
        self._guesser: Guesser = Guesser.P2
        self._word: Optional[str] = None  # Game status tied to if word is set
        self.chars_target: Optional[Set[str]] = None
        self.chars_wrong: List[str] = []
        self.full_life_count = 6
        self.chars_lives: List[str] = self.new_lives()
        self.img_map = {
            0: ''  # TODO: Add images
        }

    @property
    def word(self):
        return self._word

    @word.setter
    def word(self, value: Optional[str]):
        self.chars_wrong = []
        self.chars_lives = self.new_lives()
        self._word = value
        if value is None:
            self.chars_target = None
        else:
            self.chars_target = set(value)

    @property
    def player_setter(self):
        return self.p1 if self._guesser == Guesser.P2 else self.p2

    @property
    def player_guesser(self):
        return self.p1 if self._guesser == Guesser.P1 else self.p2

    def change_guesser(self):
        self._guesser = \
            Guesser.P1 if self._guesser == Guesser.P2 else Guesser.P2
        self.word = None

    def as_embed(self, msg=''):
        result = ''
        result += f'\n\n{msg}'
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def user_input(self, player: int, inp: str) -> Embed:
        if self.word is not None:
            # Guessing ongoing
            pass
        else:
            # Awaiting word to be set

            if player != self.player_setter:
                return self.as_embed('It is not your turn.')

            if not self.validate_word(inp):
                return self.as_embed(f'"{inp}" in not an allowed word')

            self.word = inp  # Set word
            return self.as_embed(
                f'It is <@{self.player_guesser}>\'s turn to guess')

    def new_lives(self):
        return ['♥'] * self.full_life_count

    @staticmethod
    def validate_word(word: str):
        return True  # TODO: Validate words
