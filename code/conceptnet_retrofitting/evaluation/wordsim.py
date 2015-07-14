from scipy.stats import spearmanr
import numpy as np

def evaluate(similarity_func, standard):
    actual, ideal = [], []
    for w1, w2, assoc in standard:
        ideal.append(assoc)
        actual.append(similarity_func(w1, w2))
    return spearmanr(np.array(ideal), np.array(actual))[0]

def test_all(similarity_func):
    print("wordsim-353")
    print(evaluate(similarity_func, parse_wordsim()))
    print("men-3000")
    print(evaluate(similarity_func, parse_men3000()))
    print("rg65")
    print(evaluate(similarity_func, parse_rg()))
    print("rw")
    print(evaluate(similarity_func, parse_rw()))

def parse_file(filename, sep=None, preprocess_word=None):
    with open(filename) as file:
        for line in file:
            if sep is None:
                w1, w2, val = line.strip().split()
            else:
                w1, w2, val = line.strip().split(sep)

            if preprocess_word is not None:
                w1 = preprocess_word(w1)
                w2 = preprocess_word(w2)

            yield w1, w2, float(val)


def parse_wordsim(filename='data/ws353.csv'):
    return parse_file(filename, sep=',')

def parse_men3000(filename='data/men3000.csv'):
    return parse_file(filename, preprocess_word=lambda w: w.split('-')[0])

def parse_rw(filename='data/rw.csv'):
    return parse_file(filename)

def parse_rg65(filename='data/rg-65.csv'):
    return parse_file(filename)
