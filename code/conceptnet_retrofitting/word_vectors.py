import numpy as np

from conceptnet_retrofitting.builders.label_set import LabelSet
from sklearn.preprocessing import normalize

class WordVectors:

    def __init__(self, labels, vectors, standardize=True):
        assert(len(labels) == len(vectors))
        self.labels = LabelSet(labels)
        normalize(vectors, copy=False)
        self.vectors = vectors

        if standardize:
            from conceptnet5.nodes import standardized_concept_uri
            self._standardizer = lambda label: standardized_concept_uri('en', label)
        else:
            self._standardizer = None


    def similarity(self, word1, word2):
        try:
            return self.to_vector(word1).dot(self.to_vector(word2))
        except KeyError:
            return 0

    def to_vector(self, word, return_default=True):
        if self._standardizer is None:
            return self.vectors[self.labels.index(word)]
        else:
            return self.vectors[self.labels.index(self._standardizer(word))]

    def similar_to(self, word_or_vector, num=20):
        if isinstance(word_or_vector, str):
            if self._standardizer is not None:
                word_or_vector = self._standardizer(word_or_vector)
            vec = self.to_vector(word_or_vector)
        else:
            vec = word_or_vector

        sim = self.vectors.dot(vec)
        indices = np.argsort(sim)[::-1][:num]
        return [(self.labels[index], sim[index]) for index in indices]
