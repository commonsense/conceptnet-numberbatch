import os
import math

from scipy.stats import spearmanr
import numpy as np

directory = os.path.dirname(os.path.abspath(__file__))

tests = [
    ('rw', {'filename': 'rw.csv',}),
    ('men-3000', {'filename': 'men3000-dev.csv',
                  'preprocess_word' : lambda w: w.split('-')[0]}),
    ('wordsim-353', {'filename': 'ws353.csv', 'sep':','}),
    ('wordsim-353-ar', {'filename': 'ws353.ar.csv'}, 'ar'),
    ('wordsim-353-es', {'filename': 'ws353.es.csv'}, 'es'),
    ('wordsim-353-ro', {'filename': 'ws353.ro.csv'}, 'ro'),
    ('scws', {'filename': 'scws-star.csv'}),
    ('rg-65', {'filename': 'rg-65.csv'}),
    ('rg-65-de', {'filename': 'rg-65.de.csv'}, 'de'),
    ('rg-65-fr', {'filename': 'rg-65.fr.csv'}, 'fr'),
    ('mc-30', {'filename': 'mc30.csv'}),
    ('mc-30-es', {'filename': 'mc30.es.csv'}, 'es'),
]

def test_all(similarity_func):
    for test, file_info, *optional in tests:
        lang = optional[0] if optional else None
        print(test)
        print(evaluate(similarity_func, parse_file(**file_info), lang))

def parse_file(filename, sep=None, preprocess_word=None):
    with open(os.path.join(directory, 'data', filename)) as file:
        for line in file:
            if sep is None:
                w1, w2, val, *_ = line.strip().split()
            else:
                w1, w2, val, *_ = line.strip().split(sep)

            if preprocess_word is not None:
                w1 = preprocess_word(w1)
                w2 = preprocess_word(w2)

            yield w1, w2, float(val)

def evaluate(similarity_func, standard, lang=None):
    actual, ideal = [], []
    for w1, w2, assoc in standard:
        ideal.append(assoc)
        actual.append(similarity_func(w1, w2, lang=lang))

    return spearmanr(np.array(ideal), np.array(actual))[0]

def main(labels_in, vecs_in, verbose=True):
    from conceptnet_retrofitting import loaders
    test_all(loaders.load_word_vectors(labels_in, vecs_in).similarity)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
