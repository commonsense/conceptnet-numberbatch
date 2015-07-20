import copy
from collections import defaultdict
from conceptnet_retrofitting.ninja.ninja_util import (
    Dep, DepGraph, make_ninja_file, outputs
)
from conceptnet_retrofitting.ninja.config import CONFIG

class GloveVector:

    def __init__(self, normalization='none', standardization='raw', retrofit=None,
                 filetype='npy'):
        self.normalization = normalization
        self.standardization = standardization
        self.retrofit = retrofit
        self.filetype = filetype

    def __repr__(self):
        out = ['Glove', self.normalization, self.standardization]
        if self.standardization == 'retrofit' and self.retrofit:
            out.append(self.retrofit)
        out.append(self.filetype)
        return CONFIG['datapath'] + '.'.join(out)

class GloveLabel:

    def __init__(self, standardization='raw'):
        self.standardization = standardization

    def __repr__(self):
        out = ['Glove', self.standardization, 'labels']
        return CONFIG['datapath'] + '.'.join(str(x) for x in out)


conceptnet_prefix = CONFIG['datapath']+CONFIG['conceptnet5']
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

    make_ninja_file('rules.ninja', graph)

def build_glove(graph):
    input = CONFIG['datapath'] + CONFIG['glove'] + '.txt'
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
        outputs(graph['build_glove']),
        [
            GloveVector(standardization='standardized'),
            GloveLabel('standardized')
        ],
        'standardize_vecs'
    )
    print(GloveVector(standardization='standardized'))


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
        [GloveLabel('standardized'), conceptnet_prefix+'.csv'],
        [GloveLabel('retrofit'), conceptnet_prefix+'.npz'],
        'conceptnet_to_assoc'
    )

def add_self_loops(graph):
    graph['add_self_loops'] = Dep(
        conceptnet_prefix+'.npz',
        conceptnet_prefix+'.self_loops.npz',
        'add_self_loops'
    )

def retrofit(graph):
    for norm in ['l1', 'l2', 'none']:
        graph['retrofit'][norm] = Dep(
            [
                GloveVector(standardization='standardized', normalization=norm),
                conceptnet_prefix+'.self_loops.npz'
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
        CONFIG['datapath']+'evaluations.latex',
        'tests_to_latex'
    )

if __name__ == '__main__':
    build_conceptnet_retrofitting()
