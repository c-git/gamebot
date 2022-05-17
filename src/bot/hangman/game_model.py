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


class GameModel:
    def __init__(self, p1: int, p2: int, channel: int):
        self.p1 = p1
        self.p2 = p2
        self.channel = channel
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

    @property
    def word_disp(self):
        result = ''
        for c in self.word:
            if c in self.chars_target:
                result += '_ '
            else:
                result += f'{c} '
        result = result[:-1]  # Cut off trailing space
        return result

    def as_embed(self, msg=''):
        result = ''
        if self.state == State.WAITING_FOR_GUESS:
            result += f'Set by <@{self.player_setter}>\n\n'
            result += f'`{self.word_disp}`\n\n'
            # TODO Add image to embed
            result += f'Incorrect letters guessed: ' \
                      f'{", ".join(self.chars_wrong)}\n\n'
            result += f'Lives left: {" ".join(self.chars_lives)}'
        elif self.state == State.WAITING_FOR_WORD:
            result += f'<@{self.player_setter}> please set word in the DM.'
        result += f'\n\n{msg}'
        return Embed(color=Conf.EMBED_COLOR, description=result)

    def receive_word(self, player: int, word: str) -> Embed:
        word = word.lower()
        if self.state != State.WAITING_FOR_WORD:
            raise Exception('Not waiting for a word')
        if player != self.player_setter:
            return self.as_embed('It is not your turn.')

        if not self.validate_word(word):
            return self.as_embed(f'"{word}" in not an allowed word')

        self.word = word  # Set word
        return self.as_embed(
            f'<@{self.player_guesser}>\'s turn to guess')

    def receive_guess(self, player: int, guess: str) -> Embed:
        assert len(self.chars_lives) > 0

        def check_winner() -> Optional[int]:
            if len(self.chars_target) == 0:
                return self.player_guesser
            if len(self.chars_lives) == 0:
                return self.player_setter
            return None

        guess = guess.lower()

        if self.state != State.WAITING_FOR_GUESS:
            raise Exception('Not waiting for a guess right now')

        if player != self.player_guesser:
            return self.as_embed(
                f'It is not your turn. <@{self.player_guesser}>\'s turn '
                f'to guess')

        if len(guess) != 1:
            return self.as_embed(
                "Exactly 1 letter must be guessed at a time")

        if not guess.isalpha():
            return self.as_embed("Only letters allowed")

        if guess in self.chars_wrong:
            return self.as_embed("This letter has already been guessed")

        if guess in self.chars_target:
            # Correct guess
            self.chars_target.remove(guess)
            msg = f'{guess} found'
        else:
            # Wrong guess
            self.chars_wrong.append(guess)
            self.chars_lives.pop()
            msg = f'{guess} missed'
        # Special case of win/lose
        winner: Optional[int] = check_winner()
        if winner is not None:
            # Get result before reset so display will not be affected
            result = self.as_embed(
                f'<@{winner}> WINS! The word was {self.word}')
            self.change_guesser()
            return result
        return self.as_embed(msg)

    def new_lives(self):
        return ['♥'] * self.full_life_count

    @staticmethod
    def validate_word(word: str):
        return True  # TODO: Validate words
