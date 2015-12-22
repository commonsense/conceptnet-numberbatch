#!/usr/bin/env python
from conceptnet_retrofitting.loaders import load_word2vec_bin, save_labels
import numpy as np
import sys

def main(in_file, out_labels, out_matrix):
    wv = load_word2vec_bin(in_file)
    save_labels(wv.labels, out_labels)
    np.save(out_matrix, wv.vectors)

if __name__ == '__main__':
    main(*sys.argv[1:])
