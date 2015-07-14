#!/usr/bin/env python

import numpy as np
import sys

def main(size, out_file, stdin=sys.stdin):
    vec = [float(x) for x in next(stdin).split()]
    vecs = np.zeros(shape=(size, len(vec)), dtype=float)
    vecs[0] = vec
    
    for index, line in enumerate(stdin, 1):
        vecs[index] = [float(x) for x in line.split()]
    np.save(out_file, vecs)

if __name__ == '__main__':
    main(int(sys.argv[1]), sys.argv[2])
