from conceptnet_retrofitting.ninja.ninja_util import Dep, DepGraph, make_ninja_file
from conceptnet_retrofitting.ninja.config import CONFIG

glove_prefix = CONFIG['datapath']+CONFIG['glove']

def build_conceptnet_retrofitting():
    graph = DepGraph()
    build_glove(graph)
    filter_glove(graph)
    standardize_glove(graph)
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
        graph['filter_glove'].outputs,
        [glove_prefix+'.standardized'+suffix for suffix in ['.labels', '.npy']],
        'standardize_vecs'
    )

if __name__ == '__main__':
    build_conceptnet_retrofitting()
