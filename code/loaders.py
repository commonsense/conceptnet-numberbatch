import numpy as np
from scipy import sparse

import pickle


def load_word_vecs(filename):
    return np.load(filename)


def load_sparse_assoc(filename):
    return pickle.load(filename)


def load_labels(filename):
    return [line.strip() for line in open(filename)]
