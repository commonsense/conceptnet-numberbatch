from collections import OrderedDict

import numpy as np

from conceptnet5.nodes import standardized_concept_uri
from ftfy import fix_text

class FastIndexSeq:

    def __init__(self):
        self._seq =OrderedDict()
        self._index = 0

    def append(self, item):
        self._seq[item] = self._index
        self._index += 1

    def index(self, item):
        return self._seq[item]

    def __iter__(self):
        return iter(self._seq)

    def __contains__(self, item):
        return item in self._seq

def standardize_vecs(labels, vecs):
    standardized_labels = FastIndexSeq()
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        try:
            label = standardized_concept_uri('en', label)
        except ValueError:
            continue

        vec /= (index + 1)

        if label not in standardized_labels:
            standardized_labels.append(label)
            standardized_vecs.append(vec)
        else:
            index = standardized_labels.index(label)
            standardized_vecs[index] += vec

    return list(standardized_labels), np.array(standardized_vecs)

def main(labels_in, vecs_in, labels_out, vecs_out):
    from conceptnet_retrofitting import loaders

    labels = loaders.load_labels(labels_in)
    vecs = loaders.load_vecs(vecs_in)

    labels, vecs = standardize_vecs(labels, vecs)

    loaders.save_labels(labels, labels_out)
    loaders.save_vecs(vecs, vecs_out)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
