import numpy as np

from conceptnet5.language.english import uri_and_residue
from ordered_set import OrderedSet
from conceptnet_retrofitting.word_vectors import normalize, normalize_vec


def first_ending(residue):
    chunks = residue.split(' ')
    if len(chunks) > 5:
        # Something's being inappropriately used as a term. Probably a URL.
        return ''
    for chunk in chunks:
        if '+' in chunk:
            return chunk.format('', '', '', '', '')
    return ''


def standardize_vecs(labels, vecs):
    standardized_labels = OrderedSet()
    standardized_vecs = []
    vec_denominators = []

    transformed_indices = {}

    # First pass: find indexes of fully-stemmed terms
    for index, (label, vec) in enumerate(zip(labels, vecs)):
        if index % 1000 == 0:
            print(index)
        stem, residue = uri_and_residue(label)
        ending = first_ending(residue)
        if not ending:
            transformed_indices[stem] = index

    # Second pass: find average vectors for endings
    for index, (label, vec) in enumerate(zip(labels, vecs)):
        if index % 1000 == 0:
            print(index)
        stem, residue = uri_and_residue(label)
        ending = first_ending(residue)
        if ending and stem in transformed_indices:
            print(index, label, stem, ending)
            stem_index = transformed_indices[stem]
            diff = (vec - vecs[stem_index]) / (index + 1)
            if ending not in standardized_labels:
                ending_index = standardized_labels.add(ending)
                standardized_vecs.append(diff)
                vec_denominators.append((index + 1))
            else:
                ending_index = standardized_labels.index(ending)
                standardized_vecs[ending_index] += vec
                vec_denominators[ending_index] += index + 1

    for i in range(len(standardized_vecs)):
        standardized_vecs[i] /= vec_denominators[i]

    # Third pass: handle all vectors, subtracting out difference
    # vectors from inflected versions
    for index, (label, vec) in enumerate(zip(labels, vecs)):
        if index % 1000 == 0:
            print(index)
        stem, residue = uri_and_residue(label)
        ending = first_ending(residue)
        if ending:
            diff_vec = standardized_vecs[standardized_labels.index(ending)]
            vec -= diff_vec

        scaled_vec = vec / (index + 1)

        if stem not in standardized_labels:
            standardized_labels.add(stem)
            standardized_vecs.append(vec)
        else:
            existing_index = standardized_labels.index(stem)
            standardized_vecs[existing_index] += vec

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
