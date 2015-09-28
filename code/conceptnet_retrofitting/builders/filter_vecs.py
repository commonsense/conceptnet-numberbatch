import numpy as np
import msgpack
from conceptnet_retrofitting.word_vectors import WordVectors
from wordfreq import word_frequency


def truncated_word_vecs(wv, nrows):
    return WordVectors(wv.labels[:nrows], wv.vectors[:nrows], standardizer=wv._standardizer)


def get_more_common_neighbor(concept, wv, wv2):
    print(concept, end=' ')
    if concept not in wv2.labels:
        try:
            match, weight = wv2.similar_to(wv.to_vector(concept), 1)[0]
        except KeyError:
            return ('', 0)
        print("->", match)
        return match, weight
    else:
        possibilities = wv2.similar_to(wv.to_vector(concept), num=10000)
        for poss, weight in possibilities:
            if wv2.labels.index(poss) < wv2.labels.index(concept):
                print("->", poss)
                return poss, weight
        return ('', 0)


def make_replacements(wv, labels_to_select, startrow, nrows, select_beyond_row, filter=None):
    wv2 = truncated_word_vecs(wv, nrows)
    replacements = {}
    for rownum in range(startrow, len(wv.labels)):
        item = wv.labels[rownum]
        if rownum <= select_beyond_row or item in labels_to_select:
            if filter is None or filter(item):
                neighbor, weight = get_more_common_neighbor(item, wv, wv2)
                replacements[item] = [neighbor, weight]
    wv2.replacements = replacements
    return wv2


def english_filter(label):
    return label.startswith('/c/en/') and not label.endswith('/neg')


def main(labels_in, vecs_in, selected_labels_in, labels_out, vecs_out, replacements_out):
    from conceptnet_retrofitting import loaders

    labels = loaders.load_labels(labels_in)
    vecs = loaders.load_vecs(vecs_in)
    selected_labels = loaders.load_labels(selected_labels_in)

    wv = WordVectors(labels, vecs)
    wv2 = make_replacements(wv, selected_labels, 10000, 50000, 250000, filter=english_filter)

    loaders.save_labels(wv2.labels, labels_out)
    loaders.save_vecs(wv2.vectors, vecs_out)
    loaders.save_replacements(wv2.replacements, replacements_out)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
