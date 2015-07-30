from unicodedata import normalize

from conceptnet_retrofitting.standardization.english import english_filter
from conceptnet_retrofitting.standardization.tokenizer import simple_tokenize

def standardize(text, lang='en', remove_accents=True):
    if NFD_normalize and (lang=='es' or text.startswith('/c/es/')):
        text = normalize('NFD', text).encode('ascii', errors='ignore').decode()
    if not text.startswith('/c/'):
        return standardized_concept_uri(text, lang)
    return text

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

def standardized_concept_uri(text, lang='en'):
    name = '_'.join([english_filter(token) if lang=='en' else token
                     for token in simple_tokenize(text)])
    return '/'.join(['/c', LCODE_ALIASES.get(lang, lang), name])
