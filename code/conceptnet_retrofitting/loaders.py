import numpy as np
import msgpack
import struct
import gzip
from scipy import sparse
from conceptnet_retrofitting.label_set import LabelSet
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
    with np.load(filename) as npz:
        mat = sparse.csr_matrix((npz['data'], npz['indices'], npz['indptr']), shape=npz['shape'])
    return mat


def _read_until_space(file):
    chars = []
    while True:
        newchar = file.read(1)
        if newchar == b'' or newchar == b' ':
            break
        chars.append(newchar[0])
    return bytes(chars).decode('utf-8')


def _read_vec(file, ndims):
    fmt = 'f' * ndims
    bytes_in = file.read(4 * ndims)
    values = list(struct.unpack(fmt, bytes_in))
    return np.array(values)


def load_word2vec_bin(filename):
    label_list = []
    vec_list = []
    with gzip.open(filename, 'rb') as infile:
        header = infile.readline().rstrip()
        nrows_str, ncols_str = header.split()
        nrows = int(nrows_str)
        ncols = int(ncols_str)
        for row in range(nrows):
            label = _read_until_space(infile)
            vec = _read_vec(infile, ncols)
            label_list.append(label)
            vec_list.append(vec)
    labels = LabelSet(label_list)
    mat = np.array(vec_list)
    return WordVectors(labels, mat, standardizer=lambda x: x)


def save_sparse_relations(relation_dict, filename):
    dense_dict = {}
    for rel, spmat in relation_dict.items():
        dense_dict[rel + ':data'] = spmat.data
        dense_dict[rel + ':indices'] = spmat.indices
        dense_dict[rel + ':indptr'] = spmat.indptr
        dense_dict[rel + ':shape'] = spmat.shape
    np.savez(filename, **dense_dict)


def load_sparse_relations(filename):
    sparse_rels = {}
    with np.load(filename) as npz:
        rels = [key[:-5] for key in npz if key.endswith(':data')]
        for rel in rels:
            spmat = sparse.csr_matrix(
                (npz[rel + ':data'], npz[rel + ':indices'], npz[rel + ':indptr']),
                npz[rel + ':shape'], dtype='f'
            )
            if not rel.startswith('/'):
                rel = '/' + rel
            sparse_rels[rel] = spmat
    return sparse_rels


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
        wv = WordVectors(labels, vecs, standardizer=str.lower)

    if replacements_in:
        wv.replacements = load_replacements(replacements_in)

    return wv

