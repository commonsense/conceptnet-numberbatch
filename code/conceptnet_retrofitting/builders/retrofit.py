import numpy as np
from sklearn.preprocessing import normalize


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


def relational_retrofit(word_vecs, relations, iterations=10, verbose=True, orig_weight=1):
    orig_vecs = normalize(word_vecs, norm='l2', copy=False)
    orig_vecs *= orig_weight

    vecs = np.zeros(shape=(relations[0][1].shape[0], orig_vecs.shape[1]))
    vecs[:orig_vecs.shape[0]] = orig_vecs

    for iteration in range(iterations):
        next_vecs = np.zeros(shape=vecs.shape)
        for name, sparse, dense in relations:
            if verbose:
                print('Iteration %d of %d: %s' % (iteration + 1, iterations, name))
            next_vecs += sparse.dot(vecs.dot(dense))
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
