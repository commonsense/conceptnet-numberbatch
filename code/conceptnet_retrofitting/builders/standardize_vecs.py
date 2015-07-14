from collection import OrderedDict
from conceptnet5.nodes import standardized_concept_uri

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
        return self._seq

def standardize_vecs(labels, vecs):
    standardized_labels = FastIndexSeq()
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        try:
            label = standardized_concept_uri('en', label)
        except ValueError:
            continue

        vec /= (index + 1)

        if concept not in labels_to_index:
            standardized_labels.append(label)
            standardized_vecs.append(vec)
        else:
            index = standardize_labels.index(label)
            standardize_vecs[index] += vec

    return list(standardize_labels), np.array(standardize_vecs)

def main(labels_in, vecs_in, labels_out, vecs_out):
    from conceptnet_retrofitting import loaders

    labels = loaders.load_labels(labels_in)
    vecs = loaders.load_word_vecs(vecs_in)

    labels, vecs = standardize_vecs(labels, vecs)

    loaders.save_labels(labels, labels_out)
    loaders.save_vecs(vecs, vecs_out)

if __name__ == '__main__':
    import sys
    main(*sys[1:])
