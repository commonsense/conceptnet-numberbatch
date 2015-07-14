import numpy as np
from scipy import sparse

import pickle


def load_vecs(filename):
    return np.load(filename)


def save_vecs(vecs, filename):
    return np.save(filename, vecs)


def save_csr(matrix, filename):
    np.savez(filename, data=matrix.data, indices=matrix.indices,
                indptr=matrix.indptr, shape=matrix.shape)


def load_csr(filename):
    matrix = np.load(filename)
    return sparse.csr_matrix((matrix['data'], matrix['indices'], matrix['indptr']), shape=matrix['shape'])


def load_labels(filename):
    return [line.strip() for line in open(filename, encoding='latin-1')]


def save_labels(labels, filename):
    with open(filename, mode='w') as file:
         file.write('\n'.join(labels))
