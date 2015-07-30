import re
import os


def load_range(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()

EMOJI_RANGE = load_range('emoji.txt')
NON_PUNCT_RANGE = load_range('non_punct.txt')

TOKEN_RE = re.compile("{0}|{1}+(?:'{1}+)*".format(EMOJI_RANGE, NON_PUNCT_RANGE))


def simple_tokenize(text):
    """
    A simple tokenizer that can be applied to most languages.
    It considers a word to be made of a sequence of 'token characters', an
    overly inclusive range that includes letters, Han characters, emoji, and a
    bunch of miscellaneous whatnot, but excludes most punctuation and
    whitespace.
    The single complication for the sake of English is that apostrophes are not
    considered part of the token if they appear on the edge of the character
    sequence, but they are if they appear internally. "cats'" is not a token,
    but "cat's" is.
    """
    return [token.casefold() for token in TOKEN_RE.findall(text)]
