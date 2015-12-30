import copy
from collections import defaultdict
from conceptnet_retrofitting.ninja.ninja_util import (
    Dep, DepGraph, make_ninja_file, outputs
)


CONFIG = {
    'source-data-path': 'source-data/',
    'build-data-path': 'build-data/',
    'glove-versions': ['glove12.840B.300d'],
    'word2vec-versions': ['w2v-google-news'],
    'extra-embeddings': ['combo840'],
    'neg-filters': ['jmdict', 'opencyc', 'openmind', 'verbosity', 'wiktionary', 'wordnet'],
    'pos-filters': ['wiktionary'],
    'run-filter': False,
    'retrofit-items': ['conceptnet5',
                       #'conceptnet5-minus-jmdict',
                       #'conceptnet5-minus-opencyc',
                       #'conceptnet5-minus-openmind',
                       #'conceptnet5-minus-verbosity',
                       #'conceptnet5-minus-wiktionary',
                       #'conceptnet5-minus-wordnet',
                       #'conceptnet5-wiktionary-only',
                       'ppdb-xl-lexical-standardized', 'cnet-ppdb-combined']
}
CONCEPTNET_SOURCE_FILE = 'conceptnet5.csv'


class GloveVectors:
    """
    A reference to a file containing a matrix of GloVe embeddings.
    """
    def __init__(self, version, *, normalization='none',
                 standardization='raw', retrofit=None,
                 filetype='npy'):
        self.version = version
        self.normalization = normalization
        self.standardization = standardization
        self.retrofit = retrofit
        self.filetype = filetype

    def __repr__(self):
        out = [self.version, self.normalization, self.standardization]
        if self.retrofit:
            out.append(self.retrofit)
        out.append(self.filetype)
        return CONFIG['build-data-path'] + '.'.join(out)


class GloveLabels:
    """
    A reference to a file containing the labels corresponding to a
    GloveVectors file.
    """
    def __init__(self, version, *, standardization='raw', retrofit=None):
        self.version = version
        self.standardization = standardization
        self.retrofit = retrofit

    def __repr__(self):
        out = [self.version, self.standardization]
        if self.retrofit:
            out.append(self.retrofit)
        out.append('labels')
        return CONFIG['build-data-path'] + '.'.join(str(x) for x in out)


class GloveReplacements:
    """
    A reference to a file containing the mapping from labels to simplified
    labels that corresponds to a GloveVectors file.
    """
    def __init__(self, version, *, standardization='raw', retrofit=None):
        self.version = version
        self.standardization = standardization
        self.retrofit = retrofit

    def __repr__(self):
        out = [self.version, self.standardization]
        if self.retrofit:
            out.append(self.retrofit)
        out.append('replacements.msgpack')
        return CONFIG['build-data-path'] + '.'.join(str(x) for x in out)


implicit = {
    'glove_to_vecs': ['conceptnet_retrofitting/builders/build_vecs.py'],
    'w2v_to_vecs': ['conceptnet_retrofitting/builders/build_w2v_vecs.py'],
    'filter_vecs': ['conceptnet_retrofitting/builders/filter_vecs.py'],
    'standardize_vecs': ['conceptnet_retrofitting/builders/standardize_vecs.py'],
    'l1_normalize': ['conceptnet_retrofitting/builders/l1norm.py'],
    'l2_normalize': ['conceptnet_retrofitting/builders/l2norm.py'],
    'network_to_assoc': ['conceptnet_retrofitting/builders/build_assoc.py'],
    'add_self_loops': ['conceptnet_retrofitting/builders/self_loops.py'],
    'retrofit': ['conceptnet_retrofitting/builders/retrofit.py'],
    'test': ['conceptnet_retrofitting/evaluation/wordsim.py'],
    'tests_to_latex': ['conceptnet_retrofitting/evaluation/latex_results.py'],
}


def build_conceptnet_retrofitting():
    graph = DepGraph()
    build_glove(graph)
    build_word2vec(graph)

    standardize_ppdb(graph)
    standardize_glove(graph)
    normalize_glove(graph)

    build_assoc(graph)
    filter_conceptnet(graph)
    add_self_loops(graph)
    retrofit(graph)

    test(graph)
    # latex_results(graph)

    make_ninja_file('rules.ninja', graph, implicit)


def build_glove(graph):
    for version in CONFIG['glove-versions']:
        input = CONFIG['source-data-path'] + '%s.txt' % version
        graph['build_glove']['build_glove_labels'][version] = Dep(
            input,
            GloveLabels(version=version),
            'glove_to_labels'
        )
        graph['build_glove']['build_glove_vecs'][version] = Dep(
            input,
            GloveVectors(version=version),
            'glove_to_vecs'
        )


def build_word2vec(graph):
    for version in CONFIG['word2vec-versions']:
        input = CONFIG['source-data-path'] + '%s.bin.gz' % version
        graph['build_word2vec'][version] = Dep(
            input,
            [GloveLabels(version=version), GloveVectors(version=version)],
            'w2v_to_vecs'
        )


def standardize_glove(graph):
    for version in CONFIG['glove-versions'] + CONFIG['word2vec-versions']:
        graph['standardize_glove'][version] = Dep(
            [
                GloveLabels(version=version),
                GloveVectors(version=version)
            ],
            [
                GloveLabels(version=version, standardization='standardized'),
                GloveVectors(version=version, standardization='standardized'),
            ],
            'standardize_vecs'
        )


def standardize_ppdb(graph):
    graph['standardize_ppdb'] = Dep(
        CONFIG['source-data-path'] + 'ppdb-xl-lexical.csv',
        CONFIG['build-data-path'] + 'ppdb-xl-lexical-standardized.csv',
        'standardize_assoc'
    )

    graph['combine_cnet_ppdb'] = Dep(
        [
            CONFIG['source-data-path'] + CONCEPTNET_SOURCE_FILE,
            CONFIG['build-data-path'] + 'ppdb-xl-lexical-standardized.csv'
        ],
        CONFIG['build-data-path'] + 'cnet-ppdb-combined.csv',
        'concatenate'
    )


def normalize_glove(graph):
    for version in CONFIG['glove-versions'] + CONFIG['word2vec-versions'] + CONFIG['extra-embeddings']:
        for norm in ('l1', 'l2'):
            for s13n in ('raw', 'standardized'):
                if version.startswith('combo') and s13n == 'raw':
                    continue
                graph['normalize_glove'][version][norm][s13n] = Dep(
                    GloveVectors(version=version, standardization=s13n),
                    GloveVectors(version=version, normalization=norm, standardization=s13n),
                    '%s_normalize' % norm
                )


def build_assoc(graph):
    for version in CONFIG['glove-versions'] + CONFIG['word2vec-versions'] + CONFIG['extra-embeddings']:
        for network in CONFIG['retrofit-items']:
            path = CONFIG['build-data-path']
            if network == 'conceptnet5':
                path = CONFIG['source-data-path']
            graph['network_to_assoc'][version][network] = Dep(
                [GloveLabels(version=version, standardization='standardized'), path + network + '.csv'],
                [GloveLabels(version=version, standardization='standardized', retrofit=network), CONFIG['build-data-path'] + '%s.%s.npz' % (version, network)],
                'network_to_assoc'
            )


def regex_for_dataset(dataset):
    if dataset == 'openmind':
        filter_expr = '/d/(globalmind|conceptnet)'
    else:
        filter_expr = '/d/' + dataset
    return filter_expr


def filter_conceptnet(graph):
    for dataset in CONFIG['pos-filters']:
        filter_expr = regex_for_dataset(dataset)
        graph['filter_assoc']['pos'][dataset] = Dep(
            CONFIG['source-data-path'] + CONCEPTNET_SOURCE_FILE,
            CONFIG['build-data-path'] + 'conceptnet5-%s-only.csv' % dataset,
            'filter_assoc_pos', params={'filter': filter_expr}
        )

    for dataset in CONFIG['neg-filters']:
        filter_expr = regex_for_dataset(dataset)
        graph['filter_assoc']['neg'][dataset] = Dep(
            CONFIG['source-data-path'] + CONCEPTNET_SOURCE_FILE,
            CONFIG['build-data-path'] + 'conceptnet5-minus-%s.csv' % dataset,
            'filter_assoc_neg', params={'filter': filter_expr}
        )



def add_self_loops(graph):
    for version in CONFIG['glove-versions'] + CONFIG['word2vec-versions'] + CONFIG['extra-embeddings']:
        for network in CONFIG['retrofit-items']:
            graph['add_self_loops'][network][version] = Dep(
                CONFIG['build-data-path'] + '%s.%s.npz' % (version, network),
                CONFIG['build-data-path'] + '%s.%s.self_loops.npz' % (version, network),
                'add_self_loops'
            )


def retrofit(graph):
    for network in ['conceptnet5']:
        graph['assoc_to_labels'][network] = Dep(
            CONFIG['source-data-path'] + CONCEPTNET_SOURCE_FILE,
            GloveLabels(version=network),
            'assoc_to_labels'
        )

    for version in CONFIG['glove-versions'] + CONFIG['word2vec-versions'] + CONFIG['extra-embeddings']:
        for network in CONFIG['retrofit-items']:
            for norm in ['l1', 'l2']:
                if 'conceptnet5-' in network and norm != 'l1':
                    # use only the l1 norm when trying dropping out datasets
                    continue
                graph['retrofit'][version][norm][network] = Dep(
                    [
                        GloveVectors(version=version, standardization='standardized', normalization=norm),
                        CONFIG['build-data-path'] + '%s.%s.self_loops.npz' % (version, network)
                    ],
                    GloveVectors(version=version, standardization='standardized', retrofit=network, normalization=norm),
                    'retrofit'
                )

            if CONFIG['run-filter']:
                graph['filter_vecs'][version][network] = Dep(
                    [
                        GloveLabels(version=version, standardization='standardized', retrofit=network),
                        GloveVectors(version=version, standardization='standardized', retrofit=network, normalization='l1'),
                        GloveLabels(version=network)
                    ],
                    [
                        GloveLabels(version=version, standardization='filtered', retrofit=network),
                        GloveVectors(version=version, standardization='filtered', retrofit=network, normalization='l1'),
                        GloveReplacements(version=version, standardization='filtered', retrofit=network)
                    ],
                    'filter_vecs'
                )


def test(graph):
    vector_files = defaultdict(list)

    for file in outputs(graph):
        if not isinstance(file, GloveVectors):
            continue
        vector_files[file.version, file.standardization, file.retrofit].append(file)

    for (version, standardization, retrofit), files in vector_files.items():
        if version.startswith('combo') and standardization == 'raw':
            continue
        label = GloveLabels(version=version, standardization=standardization, retrofit=retrofit)
        for file in files:
            out = copy.copy(file)
            out.filetype = 'evaluation'

            # this is a hack
            inputs = [label, file]
            if str(label) == CONFIG['build-data-path'] + 'glove.840B.300d.filtered.conceptnet5.labels':
                inputs.append(CONFIG['build-data-path'] + 'glove.840B.300d.filtered.conceptnet5.replacements.msgpack')
            graph['test']['test_%s' % file] = Dep(
                inputs, out, 'test'
            )


def latex_results(graph):
    inputs = []

    graph['latex_results'] = Dep(
        outputs(graph['test']),
        CONFIG['build-data-path'] + 'evaluations.latex',
        'tests_to_latex'
    )


if __name__ == '__main__':
    build_conceptnet_retrofitting()

