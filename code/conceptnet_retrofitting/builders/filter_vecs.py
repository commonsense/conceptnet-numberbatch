import numpy as np
from wordfreq import word_frequency

def filter_vecs(labels, vecs,
                filter_beyond_row=250000,
                end_row=1000000,
                frequency_cutoff=1e-6):

    filtered_labels = []
    filtered_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        if end_row and index > end_row:
            break

        if filter_beyond_row and \
            index > filter_beyond_row and \
            word_frequency(label, 'en') < frequency_cutoff:
            continue

        filtered_labels.append(label)
        filtered_vecs.append(vec)

    return filtered_labels, np.array(filtered_vecs)

def main(labels_in, vecs_in, labels_out, vecs_out):
    from conceptnet_retrofitting import loaders

    labels = loaders.load_labels(labels_in)
    vecs = loaders.load_vecs(vecs_in)

    labels, vecs = filter_vecs(labels, vecs)

    loaders.save_labels(labels, labels_out)
    loaders.save_vecs(vecs, vecs_out)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
