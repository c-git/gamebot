from typing import Optional, Set, Tuple

from src.conf import Conf


class Validator:
    _valid_words: Optional[Set[str]] = None

    @classmethod
    def valid_words(cls):
        if cls._valid_words is None:
            with open(Conf.DICTIONARY_FN) as f:
                words = f.readlines()
            cls._valid_words = set(words)
        return cls._valid_words

    @classmethod
    def validate_word(cls, word: str) -> Tuple[bool, Optional[str]]:
        """
        Check if the word is valid and then if not try to provide a correct word
        :param word: The word to be checked
        :return:
          (True, None)
          if word is valid else
          (False, Suggestion if possible)
        """
        pass

    @classmethod
    def is_valid_word(cls, word: str) -> bool:
        pass

    def get_suggestion(self, word: str) -> Optional[str]:
        """
        Tries to find a suggestion for a word if possible. Input should not
          be a valid word
        :param word: The word to base the suggestion on
        :return: A valid suggestion if possible else None
        """
        pass

    @classmethod
    def _clean(cls):
        """
        Method used for initial clean up of dictionary (kept for posterity)
        :return:
        """
        pass
