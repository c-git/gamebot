from enum import Enum
from typing import List, Optional, Set

from discord import Embed

from src.conf import Conf


class Guesser(Enum):
    P1 = 'P1'
    P2 = 'P2'


class State(Enum):
    WAITING_FOR_WORD = 'WAITING_FOR_WORD'
    WAITING_FOR_GUESS = 'WAITING_FOR_GUESS'


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
    def state(self):
        return State.WAITING_FOR_WORD if self.word is None else \
            State.WAITING_FOR_GUESS

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
        inp = inp.lower()

        if self.state == State.WAITING_FOR_GUESS:
            if player != self.player_guesser:
                return self.as_embed(
                    f'It is not your turn. <@{self.player_guesser}>\'s turn '
                    f'to guess')

            if len(inp) != 1:
                return self.as_embed(
                    "Exactly 1 letter must be guessed at a time")

            if not inp.isalpha():
                return self.as_embed("Only letters allowed")

            if inp in self.chars_wrong:
                return self.as_embed("This letter has already been guessed")

            if inp in self.chars_target:
                # Correct guess
                self.chars_target.remove(inp)
                msg = f'{inp} is found'
            else:
                # Wrong guess
                self.chars_wrong.append(inp)
                self.chars_lives.pop()
                msg = f'{inp} is missed'
            # TODO Handle win/loss
            return self.as_embed(msg)
        elif self.state == State.WAITING_FOR_GUESS:
            if player != self.player_setter:
                return self.as_embed('It is not your turn.')

            if not self.validate_word(inp):
                return self.as_embed(f'"{inp}" in not an allowed word')

            self.word = inp  # Set word
            return self.as_embed(
                f'<@{self.player_guesser}>\'s turn to guess')
        else:
            raise Exception('Unexpected game state')

    def new_lives(self):
        return ['♥'] * self.full_life_count

    @staticmethod
    def validate_word(word: str):
        return True  # TODO: Validate words