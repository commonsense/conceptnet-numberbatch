from collections import defaultdict
from functools import namedtuple
from os.path import exists

class Dep(namedtuple('dep', ['inputs', 'outputs', 'rule', 'params', 'use_existing'])):

    def __new__(cls, inputs, outputs, rule, params=None, use_existing=False):
        if not isinstance(inputs, list):
            inputs = [inputs]
        if not isinstance(outputs, list):
            outputs = [outputs]
        if params is None:
            params = {}

        return super().__new__(cls, inputs, outputs, rule, params, use_existing)

class DepGraph(defaultdict):

    def __init__(self):
        super().__init__(DepGraph)

def make_ninja_file(rulesfile, deps):
    with open('build.ninja', mode='w') as build_file:
        build_file.write(open(rulesfile).read())
        build_file.write('\n')
        build_file.write(to_ninja_deps(deps))
        build_file.write('\n')

def to_ninja_deps(graph):
    commands = []
    for val in graph.values():
        if isinstance(val, DepGraph):
            commands.append(to_ninja_deps(val))
        else:
            if val.use_existing and \
                all(exists(output) for output in val.outputs):
                continue

            commands.append(to_ninja_dep(val))

    return "\n\n".join(commands)

def outputs(graph):
    out = []
    for val in graph.values():
        if isinstance(val, Dep):
            out += val.outputs
        else:
            out += outputs(val)
    return out

def to_ninja_dep(dep):
    lines = []

    lines.append('build {outputs}: {rule} {inputs}'.format(
        outputs=' '.join(map(str, dep.outputs)), rule=dep.rule,
        inputs=' '.join(map(str, dep.inputs))
    ))

    for key, val in dep.params.items():
        lines.append('  {key} = {val}'.format(key=key, val=val))

    return '\n'.join(lines)
