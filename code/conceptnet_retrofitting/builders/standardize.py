from unicodedata import normalize
from conceptnet5.nodes import standardized_concept_uri

def standardize(text, lang='en', NFD_normalize=True):
    if NFD_normalize and (lang=='es' or text.startswith('/c/es/')):
        text = normalize('NFD', text).encode('ascii', errors='ignore').decode()
    if not text.startswith('/c/'):
        return standardized_concept_uri(lang, text)
    return text
