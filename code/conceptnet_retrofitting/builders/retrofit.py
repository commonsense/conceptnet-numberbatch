import numpy as np
from sklearn.preprocessing import normalize
from operator import itemgetter


def retrofit(word_vecs, sparse_assoc, iterations=10, verbose=False, orig_weight=1):
    orig_vecs = normalize(word_vecs, norm='l2', copy=False)
    orig_vecs *= orig_weight

    vecs = np.zeros(shape=(sparse_assoc.shape[0], orig_vecs.shape[1]))
    vecs[:orig_vecs.shape[0]] = orig_vecs

    for iteration in range(iterations):
        if verbose:
            print('Iteration %s of %s' % (iteration+1, iterations))

        vecs = sparse_assoc.dot(vecs)
        normalize(vecs, norm='l2', copy=False)
        vecs[:len(orig_vecs)] += orig_vecs
        vecs[:len(orig_vecs)] /= 1+orig_weight

    return vecs


def infer_orthogonal(A, B):
    aU, aS, aVt = np.linalg.svd(A, full_matrices=False)
    bU, bS, bVt = np.linalg.svd(B, full_matrices=False)
    # in Python 3.5+ this can be written as:
    #   aVt.T @ ((aU.T @ bU) @ bVt)
    return aVt.T.dot((aU.T.dot(bU)).dot(bVt))


def dense_relation_from_sparse(spmat, dmat):
    dmat2 = np.zeros((spmat.shape[0], dmat.shape[1]))
    dmat2[:dmat.shape[0]] = dmat
    coords = spmat.tocoo()
    left_rows = dmat2[coords.row] * coords.data[:, np.newaxis]
    right_rows = dmat2[coords.col] * coords.data[:, np.newaxis]
    del coords, dmat2
    sqnorms = (left_rows ** 2).sum(1)
    okay_rows = np.flatnonzero(sqnorms)
    return infer_orthogonal(left_rows[okay_rows], right_rows[okay_rows])


def dense_relation_array(word_vecs, sparse_relations):
    dmats = []
    rels = sorted(sparse_relations)
    dmats = [
        dense_relation_from_sparse(sparse_relations[rel], word_vecs)
        for rel in rels
    ]
    return np.stack(dmats, axis=0)


def relational_retrofit(word_vecs, sparse_relations, iterations=5, verbose=True, orig_weight=1):
    orig_vecs = normalize(word_vecs, norm='l2', copy=False)
    orig_vecs *= orig_weight

    vecs = np.zeros(shape=(sparse_relations[0][1].shape[0], orig_vecs.shape[1]))
    vecs[:orig_vecs.shape[0]] = orig_vecs
    sparse_list = sorted(sparse_relations.items(), key=itemgetter(0))

    for iteration in range(iterations):
        rel_array = dense_relation_array(word_vecs, sparse_relations)
        next_vecs = np.zeros(shape=vecs.shape)
        for i in range(len(sparse_list)):
            name = sparse_list[i][0]
            if verbose:
                print('Iteration %d of %d: %s' % (iteration + 1, iterations, name))
            sparse = sparse_list[i][1]
            dense = rel_array[i]
            next_vecs += sparse.dot(dense.dot(vecs))
            next_vecs += sparse.T.dot(dense.T.dot(vecs))

        normalize(next_vecs, norm='l2', copy=False)
        next_vecs[:len(orig_vecs)] += orig_vecs
        next_vecs[:len(orig_vecs)] /= 1+orig_weight
        vecs = next_vecs
        del next_vecs

    return vecs


def main(vecs_in, assoc_in, vecs_out, verbose=False):
    from conceptnet_retrofitting import loaders

    if verbose:
        print("Loading vectors")
    vecs = loaders.load_vecs(vecs_in)

    if verbose:
        print("Loading associations")
    assoc = loaders.load_csr(assoc_in)

    if verbose:
        print("Retrofitting")
    vecs = retrofit(vecs, assoc)

    if verbose:
        print("Saving")
    loaders.save_vecs(vecs, vecs_out)


if __name__ == '__main__':
    import sys
    main(sys.argv[1], sys.argv[2], sys.argv[3])
