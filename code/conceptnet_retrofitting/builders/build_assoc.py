from sklearn.preprocessing import normalize
from conceptnet_retrofitting.builders.sparse_matrix_builder import SparseMatrixBuilder
from conceptnet_retrofitting.builders.label_set import LabelSet

def build_from_conceptnet(labels, filename, verbose=True):
    """
    Generates a sparse association matrix from a conceptnet5 csv file.
    """

    mat = SparseMatrixBuilder()

    if verbose:
        print("Loading sparse associations")

    # Add pairwise associations
    data = SparseMatrixBuilder()

    with open(filename, encoding='utf-8') as infile:
        for line in infile:
            concept1, concept2, value_str = line.strip().split('\t')
            index1 = labels.add(concept1)
            index2 = labels.add(concept2)

            value = float(value_str)
            mat[index1, index2] = value
            mat[index2, index1] = value

    if verbose:
        print("Building sparse matrix")

    return mat.tocsr(shape=(len(labels), len(labels)))

def main(label_in, conceptnet_in, label_out, assoc_out):
    from conceptnet_retrofitting import loaders

    labels = LabelSet(loaders.load_labels(label_in))
    assoc = build_from_conceptnet(labels, conceptnet_in)

    loaders.save_labels(labels, label_out)
    loaders.save_csr(assoc, assoc_out)

if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
