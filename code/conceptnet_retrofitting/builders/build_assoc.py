from collections import defaultdict

from sklearn.preprocessing import normalize

from conceptnet_retrofitting.builders.sparse_matrix_builder import SparseMatrixBuilder
from conceptnet_retrofitting.builders.label_set import LabelSet
from conceptnet_retrofitting.standardization import standardize
from enum import Enum

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


def trim_negation(concept):
    if concept.endswith('/neg'):
        return concept[:-4]
    else:
        return concept


class RelType(Enum):
    forward = 1
    symmetric = 0
    backward = -1


def build_separate_relations(labels, filename, relation_map, verbose=True):
    """
    Build separate sparse matrices for each relation.
    """
    dataset_totals = defaultdict(float)
    dataset_counts = defaultdict(int)
    matrix_builders = {}

    with open(filename, encoding='utf-8') as infile:
        for line in infile:
            concept1, concept2, value_str, dataset, relation = line.strip().split('\t')
            value = float(value_str)
            dataset_label = coarse_dataset(dataset)
            dataset_totals[dataset_label] += value
            dataset_counts[dataset_label] += 1

    with open(filename, encoding='utf-8') as infile:
        rel_matrices = {}
        for line in infile:
            concept1, concept2, value_str, dataset, relation = line.strip().split('\t')
            if relation in relation_map:
                rel_target, rel_type = relation_map[relation]
                if rel_target not in matrix_builders:
                    matrix_builders[rel_target] = SparseMatrixBuilder()
                index1 = labels.add(standardize(trim_negation(concept1)))
                index2 = labels.add(standardize(trim_negation(concept2)))
                dataset_label = coarse_dataset(dataset)
                value = float(value_str) / (dataset_totals[dataset_label] / dataset_counts[dataset_label])

                if rel_type == RelType.forward or rel_type == RelType.symmetric:
                    matrix_builders[rel_target][index1, index2] = value
                if rel_type == RelType.backward or rel_type == RelType.symmetric:
                    matrix_builders[rel_target][index2, index1] = value

    return {label: mat.tocsr(shape=(len(labels), len(labels)))
            for (label, mat) in matrix_builders.items()}


def build_relations_from_conceptnet(labels, filename):
    relations = {
        '/r/RelatedTo': ('/r/RelatedTo', RelType.symmetric),
        '/r/TranslationOf': ('/r/RelatedTo', RelType.symmetric),
        '/r/Synonym': ('/r/RelatedTo', RelType.symmetric),
        '/r/SimilarTo': ('/r/RelatedTo', RelType.symmetric),

        '/r/Antonym': ('/r/Antonym', RelType.symmetric),

        '/r/DerivedFrom': ('/r/DerivedFrom', RelType.forward),
        '/r/EtymologicallyDerivedFrom': ('/r/DerivedFrom', RelType.forward),
        '/r/CompoundDerivedFrom': ('/r/DerivedFrom', RelType.forward),

        '/r/PartOf': ('/r/PartOf', RelType.forward),
        '/r/HasA': ('/r/PartOf', RelType.backward),
        '/r/MadeOf': ('/r/PartOf', RelType.backward),

        '/r/HasSubevent': ('/r/HasSubevent', RelType.forward),
        '/r/HasFirstSubevent': ('/r/HasSubevent', RelType.forward),
        '/r/HasLastSubevent': ('/r/HasSubevent', RelType.forward),
        '/r/HasPrerequisite': ('/r/HasSubevent', RelType.forward),
        '/r/IsA': ('/r/IsA', RelType.forward),
        '/r/AtLocation': ('/r/AtLocation', RelType.forward),
        '/r/UsedFor': ('/r/UsedFor', RelType.forward),
        '/r/HasProperty': ('/r/HasProperty', RelType.forward),
        '/r/Causes': ('/r/Causes', RelType.forward),
        '/r/CausesDesire': ('/r/CausesDesire', RelType.forward),
    }
    return build_separate_relations(labels, filename, relations)


def main(label_in, conceptnet_in, label_out, assoc_out):
    from conceptnet_retrofitting import loaders

    labels = LabelSet(loaders.load_labels(label_in))
    assoc = build_from_conceptnet(labels, conceptnet_in)

    loaders.save_labels(labels, label_out)
    loaders.save_csr(assoc, assoc_out)


if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
