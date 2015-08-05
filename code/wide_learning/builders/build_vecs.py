#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys

def main(out_file, stdin=sys.stdin):
    np.save(out_file, pd.read_csv(stdin, sep=' ', header=None).values)

if __name__ == '__main__':
    main(sys.argv[1])
