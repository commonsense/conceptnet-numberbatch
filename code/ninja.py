from conceptnet_retrofitting.ninja.ninja_util import Dep, DepGraph, make_ninja_file
from conceptnet_retrofitting.ninja.config import CONFIG

glove_prefix = CONFIG['datapath']+CONFIG['glove']
conceptnet_prefix = CONFIG['datapath']+CONFIG['conceptnet5']
def build_conceptnet_retrofitting():
    graph = DepGraph()
    build_glove(graph)
    #filter_glove(graph)
    standardize_glove(graph)
    l1_normalize_glove(graph)

    build_assoc(graph)
    add_self_loops(graph)
    retrofit(graph)

    make_ninja_file('rules.ninja', graph)

def build_glove(graph):
    graph['build_glove']['build_glove_labels'] = Dep(
        glove_prefix+'.txt',
        glove_prefix+'.labels',
        'glove_to_labels'
    )

    graph['build_glove']['build_glove_vecs'] = Dep(
        glove_prefix+'.txt',
        glove_prefix+'.npy',
        'glove_to_vecs'
    )

def filter_glove(graph):
    graph['filter_glove'] = Dep(
        [glove_prefix+suffix for suffix in ['.labels', '.npy']],
        [glove_prefix+'.filtered'+suffix for suffix in ['.labels', '.npy']],
        'filter_vecs'
    )

def standardize_glove(graph):
    graph['standardize_glove'] = Dep(
        [glove_prefix+suffix for suffix in ['.labels', '.npy']],
        [glove_prefix+'.standardized'+suffix for suffix in ['.labels', '.npy']],
        'standardize_vecs'
    )

def l1_normalize_glove(graph):
    graph['l1_normalize_glove'] = Dep(
        graph['standardize_glove'].outputs[1],
        glove_prefix+'.l1-normalized.npy',
        'l1_normalize'
    )

def build_assoc(graph):
    graph['conceptnet_to_assoc'] = Dep(
        [graph['standardize_glove'].outputs[0], conceptnet_prefix+'.csv'],
        [glove_prefix+'.with-assoc.labels', conceptnet_prefix+'.npz'],
        'conceptnet_to_assoc'
    )

def add_self_loops(graph):
    graph['add_self_loops'] = Dep(
        conceptnet_prefix+'.npz',
        conceptnet_prefix+'.self_loops.npz',
        'add_self_loops'
    )

def retrofit(graph):
    graph['retrofit'] = Dep(
        [glove_prefix+'.l1-normalized.npy', conceptnet_prefix+'.self_loops.npz'],
        [glove_prefix+'.retrofit.npy'],
        'retrofit'
    )

if __name__ == '__main__':
    build_conceptnet_retrofitting()
