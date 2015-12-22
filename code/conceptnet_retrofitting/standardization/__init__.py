from unicodedata import normalize
from ftfy import fix_text
from conceptnet_retrofitting.standardization.english import english_filter
from conceptnet_retrofitting.standardization.tokenizer import simple_tokenize
import re


DOUBLE_DIGIT_RE = re.compile(r'[0-9][0-9]')
DIGIT_RE = re.compile(r'[0-9]')


def standardize(text, lang='en', remove_accents=True):
    text = fix_text(text)
    if remove_accents and (lang=='es' or text.startswith('/c/es/')):
        text = normalize('NFD', text).encode('ascii', errors='ignore').decode()
    if text.startswith('/c/'):
        return replace_numbers(text)
    else:
        return standardized_concept_uri(text, lang)

LCODE_ALIASES = {
    # Pretend that all Chinese languages and variants are equivalent. This is
    # linguistically problematic, but it's also very helpful for aligning them
    # on terms where they actually are the same.
    #
    # This would mostly be a problem if ConceptNet was being used to *generate*
    # Chinese natural language text, and I don't believe it is.
    'cmn': 'zh',
    'yue': 'zh',
    'nan': 'zh',
    'zh_TW': 'zh',
    'zh_CN': 'zh',

    # An easier case: consider Bahasa Indonesia and Bahasa Malay to be the
    # same language, with code 'ms', because they're already 90% the same.
    # Many sources use 'ms' to represent the entire macrolanguage, with
    # 'zsm' to refer to Bahasa Malay in particular.
    'zsm': 'ms',
    'id': 'ms'
}


def replace_numbers(s):
    if DOUBLE_DIGIT_RE.search(s):
        return DIGIT_RE.sub('#', s)
    else:
        return s


def standardized_concept_uri(text, lang='en'):
    text = fix_text(text)
    tokens = simple_tokenize(text)
    if lang == 'en':
        tokens = english_filter(tokens)

    tokens = [replace_numbers(token) for token in tokens]
    slug = replace_numbers('_'.join(tokens))

    return '/'.join(['/c', LCODE_ALIASES.get(lang, lang), slug])
