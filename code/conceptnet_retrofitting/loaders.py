import numpy as np
from scipy import sparse

import pickle


def load_vecs(filename):
    return np.load(filename)


def save_vecs(vecs, filename):
    return np.save(filename, vecs)


def load_sparse(filename):
    return pickle.load(filename)


def save_sparse(sparse_assoc, filename):
    with open(filename, mode='wb') as file:
         pickle.dump(sparse_assoc, filename)


def load_labels(filename):
    return [line.strip() for line in open(filename)]


def save_labels(labels, filename):
    with open(filename, mode='w') as file:
         file.write('\n'.join(labels))
