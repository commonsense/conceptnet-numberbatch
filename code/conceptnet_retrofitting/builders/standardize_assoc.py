import numpy as np

from conceptnet5.nodes import standardized_concept_uri
from conceptnet_retrofitting.builders.label_set import LabelSet


def standardize_vecs(labels, vecs):
    standardized_labels = LabelSet()
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        try:
            label = standardized_concept_uri('en', label)
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


def standardize_assoc(assoc_in, assoc_out):
    """
    Take in a tab-separated file containing items that are associated with
    each other, and write it out in a form that is compatible with
    conceptnet5.csv.
    """
    with open(assoc_out, 'w', encoding='utf-8') as out:
        for line in open(assoc_in, encoding='utf-8'):
            line = line.rstrip('\n')
            if line:
                item1, item2 = line.split('\t')
                s1 = standardized_concept_uri('en', item1)
                s2 = standardized_concept_uri('en', item2)
                transformed = '%s\t%s\t1' % (s1, s2)
                print(transformed, file=out)


def main(assoc_in, assoc_out):
    standardize_assoc(assoc_in, assoc_out)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
