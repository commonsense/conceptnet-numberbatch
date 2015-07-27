import numpy as np
from scipy import sparse

from conceptnet_retrofitting.word_vectors import WordVectors

def load_vecs(filename):
    return np.load(filename)


def load_vec_memmap(filename):
    return np.load(filename, mmap_mode='r')


def save_vecs(vecs, filename):
    return np.save(filename, vecs)


def save_csr(matrix, filename):
    np.savez(filename, data=matrix.data, indices=matrix.indices,
                indptr=matrix.indptr, shape=matrix.shape)


def load_csr(filename):
    matrix = np.load(filename)
    return sparse.csr_matrix((matrix['data'], matrix['indices'], matrix['indptr']), shape=matrix['shape'])


def load_labels(filename, encoding='utf-8'):
    try:
        return [line.strip() for line in open(filename, encoding=encoding)]
    except UnicodeDecodeError:
        return[line.strip() for line in open(filename, encoding='latin-1')]

def save_labels(labels, filename):
    with open(filename, mode='w') as file:
         file.write('\n'.join(labels))

def load_word_vectors(
    labels_in='data/glove.retrofit.labels',
    vecs_in='data/glove.l1.retrofit.labels',
    ):

    labels = load_labels(labels_in)
    vecs = load_vec_memmap(vecs_in)

    if labels[0].startswith('/c/'):
        return WordVectors(labels, vecs)
    else:
        return WordVectors(labels, vecs, str.lower)
