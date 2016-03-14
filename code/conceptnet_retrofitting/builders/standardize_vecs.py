import numpy as np
import argparse
from conceptnet_retrofitting.standardization import standardize
from ordered_set import OrderedSet


def standardize_vecs(labels, vecs, merge_mode='weighted'):
    standardized_labels = OrderedSet()
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        label = standardize(label)

        if merge_mode == 'weighted':
            vec /= (index + 1)

        if label not in standardized_labels:
            standardized_labels.add(label)
            standardized_vecs.append(vec)
        else:
            if merge_mode != 'first':
                index = standardized_labels.index(label)
                standardized_vecs[index] += vec

    return list(standardized_labels), np.array(standardized_vecs)


def main(labels_in, vecs_in, labels_out, vecs_out, merge_mode):
    from conceptnet_retrofitting import loaders

    labels = loaders.load_labels(labels_in)
    vecs = loaders.load_vecs(vecs_in)

    labels, vecs = standardize_vecs(labels, vecs, merge_mode)

    loaders.save_labels(labels, labels_out)
    loaders.save_vecs(vecs, vecs_out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('labels_in')
    parser.add_argument('vecs_in')
    parser.add_argument('labels_out')
    parser.add_argument('vecs_out')
    parser.add_argument('-m', '--merge_mode', default='weighted')
    args = parser.parse_args()
    main(args.labels_in, args.vecs_in, args.labels_out, args.vecs_out, args.merge_mode)
