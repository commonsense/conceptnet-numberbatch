import copy
from collections import defaultdict
from conceptnet_retrofitting.ninja.ninja_util import (
    Dep, DepGraph, make_ninja_file, outputs
)
from conceptnet_retrofitting.ninja.config import CONFIG


# TODO: clean up these classes; their names are confusing and I'm not sure
# why they need to be classes anyway

class GloveVector:
    def __init__(self, normalization='none', standardization='raw', retrofit=None,
                 filetype='npy'):
        self.normalization = normalization
        self.standardization = standardization
        self.retrofit = retrofit
        self.filetype = filetype

    def __repr__(self):
        out = ['glove', self.normalization, self.standardization]
        if self.standardization == 'retrofit' and self.retrofit:
            out.append(self.retrofit)
        out.append(self.filetype)
        return CONFIG['build-data-path'] + '.'.join(out)


class GloveLabel:
    def __init__(self, standardization='raw'):
        self.standardization = standardization

    def __repr__(self):
        out = ['glove', self.standardization, 'labels']
        return CONFIG['build-data-path'] + '.'.join(str(x) for x in out)


implicit = {
    'glove_to_vecs': ['conceptnet_retrofitting/builders/build_vecs.py'],
    'filter_vecs': ['conceptnet_retrofitting/builders/filter_vecs.py'],
    'standardize_vecs': ['conceptnet_retrofitting/builders/standardize_vecs.py'],
    'l1_normalize': ['conceptnet_retrofitting/builders/l1norm.py'],
    'l2_normalize': ['conceptnet_retrofitting/builders/l2norm.py'],
    'conceptnet_to_assoc': ['conceptnet_retrofitting/builders/build_assoc.py'],
    'add_self_loops': ['conceptnet_retrofitting/builders/self_loops.py'],
    'retrofit': ['conceptnet_retrofitting/builders/retrofit.py'],
    'test': ['conceptnet_retrofitting/evaluation/wordsim.py'],
    'tests_to_latex': ['conceptnet_retrofitting/builders/latex_results.py'],
}

def build_conceptnet_retrofitting():
    graph = DepGraph()
    build_glove(graph)

    l1_normalize_raw_glove(graph)
    l2_normalize_raw_glove(graph)

    standardize_glove(graph)
    l1_normalize_glove(graph)
    l2_normalize_glove(graph)

    build_assoc(graph)
    add_self_loops(graph)
    retrofit(graph)

    test(graph)
    latex_results(graph)

    make_ninja_file('rules.ninja', graph, implicit)

def build_glove(graph):
    input = CONFIG['source-data-path'] + CONFIG['glove'] + '.txt'
    graph['build_glove']['build_glove_labels'] = Dep(
        input,
        GloveLabel(),
        'glove_to_labels'
    )

    graph['build_glove']['build_glove_vecs'] = Dep(
        input,
        GloveVector(),
        'glove_to_vecs'
    )


def standardize_glove(graph):
    graph['standardize_glove'] = Dep(
        [
            GloveLabel(),
            GloveVector()
        ],
        [
            GloveLabel('standardized'),
            GloveVector(standardization='standardized'),
        ],
        'standardize_vecs'
    )


def l2_normalize_raw_glove(graph):
    graph['l2_normalize_raw_glove'] = Dep(
        GloveVector(),
        GloveVector(normalization='l2'),
        'l2_normalize'
    )

def l1_normalize_raw_glove(graph):
    graph['l1_normalize_raw_glove'] = Dep(
        GloveVector(),
        GloveVector(normalization='l1'),
        'l1_normalize'
    )

def l2_normalize_glove(graph):
    graph['l2_normalize_glove'] = Dep(
        GloveVector(standardization='standardized'),
        GloveVector(standardization='standardized', normalization='l2'),
        'l2_normalize'
    )

def l1_normalize_glove(graph):
    graph['l1_normalize_glove'] = Dep(
        GloveVector(standardization='standardized'),
        GloveVector(standardization='standardized', normalization='l1'),
        'l1_normalize'
    )

def build_assoc(graph):
    graph['conceptnet_to_assoc'] = Dep(
        [GloveLabel('standardized'), CONFIG['source-data-path'] + CONFIG['conceptnet'] + '.csv'],
        [GloveLabel('retrofit'), CONFIG['build-data-path'] + CONFIG['conceptnet'] + '.npz'],
        'conceptnet_to_assoc'
    )

def add_self_loops(graph):
    conceptnet_prefix = CONFIG['build-data-path'] + CONFIG['conceptnet']
    graph['add_self_loops'] = Dep(
        conceptnet_prefix + '.npz',
        conceptnet_prefix + '.self_loops.npz',
        'add_self_loops'
    )

def retrofit(graph):
    conceptnet_prefix = CONFIG['build-data-path'] + CONFIG['conceptnet']
    for norm in ['l1', 'l2', 'none']:
        graph['retrofit'][norm] = Dep(
            [
                GloveVector(standardization='standardized', normalization=norm),
                conceptnet_prefix + '.self_loops.npz'
            ],
            GloveVector(standardization='retrofit', normalization=norm),
            'retrofit'
        )

def test(graph):
    vector_files = defaultdict(list)
    for file in outputs(graph):
        if not isinstance(file, GloveVector):
            continue
        vector_files[file.standardization].append(file)

    for standardization, files in vector_files.items():
        label = GloveLabel(standardization)
        for file in files:
            out = copy.copy(file)
            out.filetype = 'evaluation'

            graph['test']['test_%s'%file] = Dep(
                [label, file], out, 'test'
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
