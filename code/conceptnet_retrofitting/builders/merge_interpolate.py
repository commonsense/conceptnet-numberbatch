import numpy as np
from sklearn.preprocessing import normalize
from operator import itemgetter
from ordered_set import OrderedSet
from conceptnet_retrofitting import loaders
from conceptnet_retrofitting.word_vectors import WordVectors


def merge_interpolate(wv1, wv2, extra_labels, verbose=False):
    common_vocab = wv1.labels & wv2.labels
    interpolated_vocab_1 = (wv1.labels - wv2.labels) & extra_labels
    interpolated_vocab_2 = (wv2.labels - wv1.labels) & extra_labels
    assert isinstance(common_vocab, OrderedSet)

    n1, k1 = wv1.vectors.shape
    n2, k2 = wv2.vectors.shape
    nmerged = len(common_vocab)

    if verbose:
        print("Joining common vocabulary")

    joined_vecs = np.zeros((nmerged, k1 + k2))
    for idx, word in enumerate(common_vocab):
        joined_vecs[idx, :k1] = wv1.to_vector(word)
        joined_vecs[idx, k1:] = wv2.to_vector(word)

    if verbose:
        print("Reducing dimensionality of common vocabulary")

    U, S, Vt = np.linalg.svd(joined_vecs, full_matrices=False)
    np.savez('merge_interpolate.npz', U=U, S=S, Vt=Vt, joined_vecs=joined_vecs)
    wv = WordVectors(common_vocab, U * S, standardizer=wv1._standardizer)

    # Output the word vectors, as well as V for diagnostic purposes
    return wv, Vt.T


def main(labels1, vecs1, labels2, vecs2, more_labels, labels_out, vecs_out, verbose=False):
    if verbose:
        print("Loading vectors")
    wv1 = loaders.load_word_vectors(labels1, vecs1)
    wv2 = loaders.load_word_vectors(labels2, vecs2)
    extra_labels = loaders.load_labels(more_labels)
    merged, V = merge_interpolate(wv1, wv2, extra_labels)

    if verbose:
        print("Saving")
    loaders.save_labels(merged.labels, vecs_out)
    loaders.save_vecs(merged.vectors, vecs_out)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])

