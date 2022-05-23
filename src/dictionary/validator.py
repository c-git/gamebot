from typing import Optional, Set, Tuple

from textblob import TextBlob

from src.conf import Conf


class Validator:
    _valid_words: Optional[Set[str]] = None

    @classmethod
    def valid_words(cls):
        if cls._valid_words is None:
            with open(Conf.DICTIONARY_FN) as f:
                words = f.readlines()
            # -1 to strip off delimiter
            cls._valid_words = set([x[:-1] for x in words])
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
        if cls.is_valid_word(word):
            return True, None
        else:
            return False, cls.get_suggestion(word)

    @classmethod
    def is_valid_word(cls, word: str) -> bool:
        return word in cls.valid_words()

    @classmethod
    def get_suggestion(cls, word: str) -> Optional[str]:
        """
        Tries to find a suggestion for a word if possible. Input should not
          be a valid word
        :param word: The word to base the suggestion on
        :return: A valid suggestion if possible else None
        """
        result = str(TextBlob(word).correct())
        return result if cls.is_valid_word(result) else None

    @classmethod
    def _clean(cls):
        """
        Method used for initial clean up of dictionary (kept for posterity)
        :return:
        """
        with open(Conf.DICT_SHORT_WORDS_FN) as f:
            allowed_short_words = set(f.readlines())
        with open(Conf.DICTIONARY_FN) as f:
            words = f.readlines()
        replacements = []
        unique = set()  # used to filter out duplicate words
        for word in words:
            word = word.lower()  # Make all words lower case

            # Remove suffixes
            try:
                pos = word.index('/')
                word = word[:pos] + '\n'
            except ValueError:
                pass

            if not word[:-1].isalpha():
                continue  # remove words that don't only contain letters

            if word not in unique and \
                    (len(word) > 5 or
                     word in allowed_short_words):
                replacements.append(word)
                unique.add(word)
        with open(Conf.DICTIONARY_FN, 'w') as f:
            f.writelines(replacements)
