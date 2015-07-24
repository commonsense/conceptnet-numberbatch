import os
import math

from scipy.stats import spearmanr
import numpy as np

directory = os.path.dirname(os.path.abspath(__file__))

def evaluate(similarity_func, standard):
    actual, ideal = [], []
    for w1, w2, assoc in standard:
        ideal.append(assoc)
        actual.append(similarity_func(w1, w2))

    return spearmanr(np.array(ideal), np.array(actual))[0]

def test_all(similarity_func):
    print("rw")
    print(evaluate(similarity_func, parse_rw()))
    print("men-3000")
    print(evaluate(similarity_func, parse_men3000()))
    print("wordsim-353")
    print(evaluate(similarity_func, parse_wordsim353()))
    print("scws")
    print(evaluate(similarity_func, parse_scws()))
    print("rg-65")
    print(evaluate(similarity_func, parse_rg65()))
    print("mc-30")
    print(evaluate(similarity_func, parse_mc30()))

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


def parse_wordsim353(filename='ws353.csv'):
    return parse_file(filename, sep=',')

def parse_men3000(filename='men3000-dev.csv'):
    return parse_file(filename, preprocess_word=lambda w: w.split('-')[0])

def parse_rw(filename='rw.csv'):
    return parse_file(filename)

def parse_rg65(filename='rg-65.csv'):
    return parse_file(filename)

def parse_mc30(filename='mc30.csv'):
    return parse_file(filename)

def parse_scws(filename='scws.csv'):
    with open(os.path.join(directory, 'data', filename)) as file:
        for line in file:
            parts = line.strip().split('\t')
            w1 = parts[1]
            w2 = parts[3]
            val = float(parts[7])
            if w1 != w2:
                yield w1, w2, float(val)

def main(labels_in, vecs_in, verbose=True):
    from conceptnet_retrofitting import loaders
    test_all(loaders.load_word_vectors(labels_in, vecs_in).similarity)

if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2])
