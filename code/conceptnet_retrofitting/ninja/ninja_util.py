from collections import defaultdict
from functools import namedtuple


class Dep(namedtuple('dep', ['inputs', 'outputs', 'rule', 'params'])):

    def __new__(cls, inputs, outputs, rule, params=None):
        if isinstance(inputs, str):
            inputs = [inputs]
        if isinstance(outputs, str):
            outputs = [outputs]
        if params is None:
            params = {}

        return super().__new__(inputs, outputs, rule, args)

class DepGraph(defaultdict):

    def __init__(self):
        super().__init__(recursive_dict)

def make_ninja_file(rulesfile, deps):
    with open('build.ninja') as build_file:
        build_file.write(open(rulesfile).read())
        build_file.write(to_ninja_deps(deps))

def to_ninja_deps(graph):
    rules = []
    for val in graph.values():
        if isinstance(val, DepGraph):
            commands += build_ninja(val)
        else:
            commands.append(to_ninja_dep(val))

    return "\n\n".join(rules)

def to_ninja_dep(dep):
    lines = []

    lines.append()'build {outputs}: {rule} {inputs}{extra}'.format(
        outputs=dep.outputs, rule=dep.rule, inputs=dep.inputs, extra=extrastr
    ))

    for key, val in params.items():
        lines.append(''  {key} = {val}''.format(key=key, val=val))

    return '\n'.join(lines)
