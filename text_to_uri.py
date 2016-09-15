"""
This Python module provides just the code from the 'conceptnet5' module that
you need to represent terms, possibly with multiple words, as ConceptNet URIs.

It depends on 'wordfreq', a Python 3 library, so it can tokenize multilingual
text consistently: https://pypi.org/project/wordfreq/

Example:

>>> standardized_uri('es', 'ayudar')
'/c/es/ayudar'
>>> standardized_uri('en', 'a test phrase')
'/c/en/test_phrase'
>>> standardized_uri('en', '24 hours')
'/c/en/##_hours'
"""
import wordfreq
import re


# English-specific stopword handling
STOPWORDS = ['the', 'a', 'an']
DROP_FIRST = ['to']
DOUBLE_DIGIT_RE = re.compile(r'[0-9][0-9]')
DIGIT_RE = re.compile(r'[0-9]')


def standardized_uri(language, term):
    """
    Get a URI that is suitable to label a row of a vector space, by making sure
    that both ConceptNet's and word2vec's normalizations are applied to it.

    'language' should be a BCP 47 language code, such as 'en' for English.

    If the term already looks like a ConceptNet URI, it will only have its
    sequences of digits replaced by #. Otherwise, it will be turned into a
    ConceptNet URI in the given language, and then have its sequences of digits
    replaced.
    """
    if not (term.startswith('/') and term.count('/') >= 2):
        term = _standardized_concept_uri(language, term)
    return replace_numbers(term)


def english_filter(tokens):
    """
    Given a list of tokens, remove a small list of English stopwords. This
    helps to work with previous versions of ConceptNet, which often provided
    phrases such as 'an apple' and assumed they would be standardized to
	'apple'.
    """
    non_stopwords = [token for token in tokens if token not in STOPWORDS]
    while non_stopwords and non_stopwords[0] in DROP_FIRST:
        non_stopwords = non_stopwords[1:]
    if non_stopwords:
        return non_stopwords
    else:
        return tokens


def replace_numbers(s):
    """
    Replace digits with # in any term where a sequence of two digits appears.

    This operation is applied to text that passes through word2vec, so we
    should match it.
    """
    if DOUBLE_DIGIT_RE.search(s):
        return DIGIT_RE.sub('#', s)
    else:
        return s


def _standardized_concept_uri(language, term):
    if language == 'en':
        token_filter = english_filter
    else:
        token_filter = None
    language = language.lower()
    norm_text = _standardized_text(term, token_filter)
    return '/c/{}/{}'.format(language, norm_text)


def _standardized_text(text, token_filter):
    tokens = simple_tokenize(text.replace('_', ' '))
    if token_filter is not None:
        tokens = token_filter(tokens)
    return '_'.join(tokens)


def simple_tokenize(text):
    """
    Tokenize text using the default wordfreq rules.
    """
    return wordfreq.tokenize(text, 'xx')


