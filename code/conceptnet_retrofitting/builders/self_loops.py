import numpy as np

def self_loops(assoc):

    diagonal = np.diag_indices(assoc.shape[0])

    assoc = assoc.todok()
    assoc[diagonal] = assoc.sum(axis=1).T[0]
    return assoc.tocsr()

def main(assoc_in, assoc_out):
    from conceptnet_retrofitting import loaders

    assoc = loaders.load_csr(assoc_in)

    assoc = self_loops(assoc)

    loaders.save_csr(assoc, assoc_out)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
