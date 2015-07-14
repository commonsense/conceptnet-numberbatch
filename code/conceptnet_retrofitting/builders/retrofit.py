import numpy as np
from sklearn.preprocessing import normalize

def retrofit(word_vecs, sparse_assoc, iterations=8, verbose=True, orig_weight=1):

    orig_vecs = normalize(word_vecs, norm='l2', copy=False)

    vecs = np.zeros(shape=(sparse_assoc.shape[0], orig_vecs.shape[1]))
    vecs[:orig_vecs.shape[0]] = orig_vecs

    for iteration in range(iterations):
        if verbose:
            print('Iteration %s of %s' % (iteration+1, iterations))

        new_vecs = sparse_assoc.dot(vecs)
        normalize(new_vecs, norm='l2', copy=False)
        new_vecs[:len(orig_vecs)] += orig_weight*orig_vecs
        new_vecs[:len(orig_vecs)] /= 1+orig_weight

        if verbose:
            print("Average difference: %s" % np.mean(np.abs(new_vecs - vecs)))

        vecs = new_vecs

    return vecs

def main(vecs_in, assoc_in, vecs_out, verbose=True):
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
    main(*sys.argv[1:])
