import numpy as np

from conceptnet_retrofitting.builders.standardize import standardize
from conceptnet_retrofitting.builders.label_set import LabelSet

def standardize_vecs(labels, vecs):
    standardized_labels = LabelSet()
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        try:
            label = standardize(label)
        except ValueError:
            continue

        vec /= (index + 1)

        if label not in standardized_labels:
            standardized_labels.add(label)
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
