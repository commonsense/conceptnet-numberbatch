import numpy as np

from conceptnet_retrofitting.standardization import standardize
from ordered_set import OrderedSet
from sklearn.preprocessing import normalize


def weighted_3cosmul(v1, v2, v3, vectors, power=2):
    numer1 = vectors.dot(v3) + 1
    numer2 = vectors.dot(v2) + 1
    denom = vectors.dot(v1) + 1
    return (numer1 ** power * numer2) / denom


def rank3_inner_product(vec, array3):
    return (array3 * vec[:, np.newaxis, np.newaxis]).sum(0)


def normalize_vec(vec):
    return normalize(vec.reshape(1, -1))[0]


class WordVectors:
    def __init__(self, labels, vectors, replacements=None, standardizer=standardize):
        assert(len(labels) == len(vectors))
        self.labels = OrderedSet(labels)
        if not isinstance(vectors, np.memmap):
            normalize(vectors, copy=False)
        self.vectors = vectors
        self.replacements = replacements
        self._standardizer = standardizer
        self._mean_vec = np.mean(self.vectors, axis=0)

    def truncate(self, size):
        return WordVectors(
            list(self.labels)[:size],
            self.vectors[:size],
            self.replacements,
            self._standardizer
        )

    def similarity(self, word1, word2, lang=None):
        try:
            return self.to_vector(word1, lang).dot(self.to_vector(word2, lang))
        except KeyError:
            return 0

    def to_vector(self, word, lang=None, default_zero=False) -> np.ndarray:
        if isinstance(word, list):
            vec = np.zeros(self.vectors.shape[1])
            for actual_word, weight in word:
                vec += self.to_vector(actual_word, lang=lang)
            return normalize_vec(vec)

        if self._standardizer is not None:
            if self._standardizer is standardize and \
                lang is not None:
                word = self._standardizer(word, lang=lang)
            else:
                word = self._standardizer(word)

        max_sim = 1.
        if self.replacements and word in self.replacements:
            while word not in self.labels:
                word, sim = self.replacements[word]
                #max_sim *= np.sqrt(sim)

        if default_zero and word not in self.labels:
            return np.zeros(self.vectors.shape[1])
        vec = normalize_vec(self.vectors[self.labels.index(word)])
        return vec * max_sim

    def similar_to(self, word_or_vector, num=20, only=None):
        if isinstance(self.vectors, np.memmap):
            self.vectors = normalize(self.vectors)

        if isinstance(word_or_vector, str):
            vec = self.to_vector(word_or_vector)
        else:
            vec = word_or_vector

        sim = self.vectors.dot(vec)
        indices = np.argsort(sim)[::-1]

        out = []
        for index in indices:
            if len(out) == num:
                return out
            if only is None or only(self.labels[index]):
                out.append((self.labels[index], sim[index]))

        return out

    def which_relation(self, rel_array, v1, v2):
        if isinstance(v1, str):
            v1 = self.to_vector(v1)
        if isinstance(v2, str):
            v2 = self.to_vector(v2)
        avg_rel = self._mean_vec.dot(rel_array.dot(self._mean_vec))
        rels = v2.dot(rel_array.dot(v1))
        diff = np.maximum(0, rels - avg_rel) ** 2
        return diff / np.sum(diff)

    def analogy_values(self, rel_array, c1, c2, c3, vector_choices):
        # Convert the input concepts to vectors
        v1, v2, v3 = [self.to_vector(c, default_zero=True) for c in (c1, c2, c3)]
        # relA and relB are vectors whose length is the number of relations.
        # They indicate the relative weight with which each relation holds
        # between appropriate pairs of input concepts.
        relA = self.which_relation(rel_array, v1, v2)
        relB = self.which_relation(rel_array, v1, v3)
        # relAr and relBr are matrices that use these combinations of
        # relations to convert one vector into another.
        relAr = rank3_inner_product(relA, rel_array)
        relBr = rank3_inner_product(relB, rel_array)

        # rv1 is the vector that's related to v1 by these relations, and so on.
        rv1 = (relAr + relBr).dot(v1)
        rv2 = relBr.dot(v2)
        rv3 = relAr.dot(v3)
        ratings = weighted_3cosmul(rv1, rv2, rv3, vector_choices)
        return ratings

    def rank_analogies(self, rel_array, c1, c2, c3, only=None, num=20):
        ratings = self.analogy_values(rel_array, c1, c2, c3, self.vectors)
        indices = np.argsort(ratings)[::-1]

        out = []
        for index in indices:
            if len(out) >= num:
                return out
            if only is None or only(self.labels[index]):
                out.append((self.labels[index], ratings[index]))
        return out

    def rate_analogy(self, rel_array, c1, c2, c3, c4):
        v4 = self.to_vector(c4)
        return self.analogy_values(rel_array, c1, c2, c3, v4)
