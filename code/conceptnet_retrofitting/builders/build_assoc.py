from collections import defaultdict

from sklearn.preprocessing import normalize

from conceptnet_retrofitting.builders.sparse_matrix_builder import SparseMatrixBuilder
from conceptnet_retrofitting.builders.label_set import LabelSet
from conceptnet_retrofitting.standardization import standardize

def coarse_dataset(dataset):
    if '/' not in dataset:
        return dataset
    if dataset.startswith('/d/globalmind') or dataset.startswith('/d/dbpedia'):
        dataset = '/d/conceptnet'
    dataset_label = dataset.split('/')[2]
    return dataset_label


def build_from_conceptnet(labels, filename, verbose=True):
    """
    Generates a sparse association matrix from a conceptnet5 csv file.
    """

    mat = SparseMatrixBuilder()

    # Scale the values by dataset
    dataset_totals = defaultdict(float)
    dataset_counts = defaultdict(int)
    with open(filename, encoding='utf-8') as infile:
        for line in infile:
            concept1, concept2, value_str, dataset, relation = line.strip().split('\t')
            value = float(value_str)
            dataset_label = coarse_dataset(dataset)
            dataset_totals[dataset_label] += value
            dataset_counts[dataset_label] += 1

    with open(filename, encoding='utf-8') as infile:
        for line in infile:
            concept1, concept2, value_str, dataset, relation = line.strip().split('\t')
            index1 = labels.add(standardize(concept1))
            index2 = labels.add(standardize(concept2))

            dataset_label = coarse_dataset(dataset)
            value = float(value_str) / (dataset_totals[dataset_label] / dataset_counts[dataset_label])
            mat[index1, index2] = value
            mat[index2, index1] = value

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
