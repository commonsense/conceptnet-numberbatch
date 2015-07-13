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

def parse_wordsim(filename='data/ws353.csv'):
    with open(filename) as file:
        next(file) # skip header
        for line in file:
            w1, w2, val = line.strip().split(',')
            yield w1, w2, float(val)

def parse_men3000(filename='data/men3000.csv'):
    with open(filename) as file:
        for line in file:
            w1, w2, val = line.strip().split()
            yield w1.split('-')[0], w2.split('-')[0], float(val)

def parse_rw(filename='data/rw.csv'):
    with open(filename) as file:
        for line in file:
            w1, w2, avg, *_ = line.split()
            yield w1, w2, float(avg)

def parse_rg65(filename='data/rg-65.csv'):
    with open(filename) as file:
        for line in file:
            w1, w2, val = line.strip().split()
            yield w1, w2, float(val)
