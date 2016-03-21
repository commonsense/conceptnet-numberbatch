import numpy as np
from sklearn.preprocessing import normalize
from operator import itemgetter
from ordered_set import OrderedSet
from conceptnet_retrofitting import loaders
from conceptnet_retrofitting.word_vectors import WordVectors


def merge_interpolate(wv1, wv2, extra_labels, verbose=False):
    common_vocab = wv1.labels & wv2.labels
    common_vocab_2 = wv2.labels & wv1.labels
    interpolated_vocab_1 = (wv1.labels - wv2.labels) & extra_labels
    interpolated_vocab_2 = (wv2.labels - wv1.labels) & extra_labels
    assert isinstance(common_vocab, OrderedSet)

    n1, k1 = wv1.vectors.shape
    n2, k2 = wv2.vectors.shape
    nmerged = len(common_vocab)

    if verbose:
        print("Joining common vocabulary")

    joined_vecs = np.zeros((nmerged, k1 + k2))
    joined_vecs_2 = np.zeros((nmerged, k1 + k2))

    for idx, word in enumerate(common_vocab):
        joined_vecs[idx, :k1] = wv1.to_vector(word)
        joined_vecs[idx, k1:] = wv2.to_vector(word)
        idx2 = common_vocab_2.index(word)
        joined_vecs_2[idx2, :k1] = joined_vecs[idx, :k1]
        joined_vecs_2[idx2, k1:] = joined_vecs[idx, k1:]

    wv_joined = WordVectors(common_vocab, joined_vecs)
    wv_sample_1 = WordVectors(common_vocab[:50000], joined_vecs[:50000, :k1])
    wv_sample_2 = WordVectors(common_vocab_2[:50000], joined_vecs_2[:50000, k1:])

    new_labels = []
    new_vectors = np.zeros((len(interpolated_vocab_1) + len(interpolated_vocab_2), k1 + k2))

    for idx, word in enumerate(interpolated_vocab_1):
        if idx % 100 == 0:
            print("Adding extra vocab set 1: %d/%d" % (idx, len(interpolated_vocab_1)))
        vec_in = wv1.to_vector(word)
        sim = wv_sample_1.similar_to(vec_in, num=5)
        vec = wv_joined.to_vector(sim)
        vec[:k1] = vec_in

        new_vectors[len(new_labels)] = vec
        new_labels.append(word)

    for idx, word in enumerate(interpolated_vocab_2):
        if idx % 100 == 0:
            print("Adding extra vocab set 2: %d/%d" % (idx, len(interpolated_vocab_2)))
        vec_in = wv2.to_vector(word)
        sim = wv_sample_2.similar_to(vec_in, num=5)
        vec = wv_joined.to_vector(sim)
        vec[k1:] = vec_in

        new_vectors[len(new_labels)] = vec
        new_labels.append(word)

    full_labels = OrderedSet(common_vocab.items + new_labels)
    full_vectors = np.concatenate((joined_vecs, new_vectors), axis=0)
    del wv_joined
    del wv_sample_1
    del wv_sample_2
    del joined_vecs_2

    if verbose:
        print("Reducing dimensionality of common vocabulary")

    U, S, Vt = np.linalg.svd(full_vectors, full_matrices=False)
    wv = WordVectors(full_labels, (U * np.sqrt(S))[:, :k1], standardizer=wv1._standardizer)

    # Output the word vectors, as well as V for diagnostic purposes
    return wv, Vt.T[:, :k1]


def main(labels1, vecs1, labels2, vecs2, more_labels, labels_out, vecs_out, verbose=False):
    if verbose:
        print("Loading vectors")
    wv1 = loaders.load_word_vectors(labels1, vecs1)
    wv2 = loaders.load_word_vectors(labels2, vecs2)
    extra_labels = loaders.load_labels(more_labels)
    merged, V = merge_interpolate(wv1, wv2, extra_labels)

    if verbose:
        print("Saving")
    loaders.save_labels(merged.labels, labels_out)
    loaders.save_vecs(merged.vectors, vecs_out)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])

