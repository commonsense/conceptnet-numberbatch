import numpy as np
from sklearn import normalize

def retrofit(word_vecs, sparse_assoc, iterations=8, verbose=True, orig_weight=1):
    orig_vecs = normalize(word_vecs, norm='l2')
    vecs = orig_vecs

    if verbose:
        print("Retrofitting")

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
