from conceptnet_retrofitting.builders.label_set import LabelSet
from sklearn.preprocessing import normalize

class AssocSpace:

    def __init__(self, labels, vectors, standardize=True):
        self.labels = LabelSet(labels)
        normalize(vectors, norm='l2', axis=1, copy=False)
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

    def to_vector(self, word):
        if self._standardizer is None:
            return self.vectors[self.labels.index(word)]
        else:
            return self.vectors[self.labels.index(self._standardizer(word))]
