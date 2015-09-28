import numpy as np
import msgpack
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


def load_replacements(filename):
    return msgpack.load(open(filename, 'rb'), encoding='utf-8')


def save_replacements(replacements, filename):
    with open(filename, 'wb') as out:
        msgpack.dump(replacements, out)


def save_labels(labels, filename):
    with open(filename, mode='w') as file:
         file.write('\n'.join(labels))


def load_word_vectors(labels_in, vecs_in, replacements_in=None, memmap=True):
    labels = load_labels(labels_in)
    if memmap:
        vecs = load_vec_memmap(vecs_in)
    else:
        vecs = load_vecs(vecs_in)

    if labels[0].startswith('/c/'):
        wv = WordVectors(labels, vecs)
    else:
        wv = WordVectors(labels, vecs, str.lower)
    
    if replacements_in:
        wv.replacements = load_replacements(replacements_in)
    
    return wv

