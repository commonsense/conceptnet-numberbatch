from collections import OrderedDict, defaultdict
import pandas as pd

def main(in_files, out_file):
    in_files.sort(key=order_names)

    data = OrderedDict((k, []) for k in parse_evaluation(in_files[0]))
    vectors = [to_simple_name(filename) for filename in in_files]

    for filename in in_files:
        for test, score in parse_evaluation(filename).items():
            data[test].append(score)

    df = pd.DataFrame(data, index=vectors)
    with open(out_file, mode='w') as file:
        file.write(df.to_latex())

def parse_evaluation(filename):
    results = OrderedDict()
    with open(filename) as file:
        name = None
        for line in file:
            line = line.strip()
            if name is None:
                name = line
            else:
                results[name] = float(line)
                name = None
    return results

def to_simple_name(filename):
    sections = filename.split('/')[-1].split('.')
    assert sections[-1] == 'evaluation'


    simple_name = []
    if 'retrofit' in sections:
        simple_name.append('retrofitted')
    elif 'raw' in sections or len(sections) == 5:
        simple_name.append('raw')
    else:
        simple_name.append('standardized')

    if 'l1' in sections or 'l1-normalized' in sections:
        simple_name.append('(l1)')
    elif 'l2' in sections or 'l2-normalized' in sections:
        simple_name.append('(l2)')

    return ' '.join(simple_name)

def order_names(filename):
    out = [0, 0]
    simple = to_simple_name(filename)

    if simple.startswith('retrofitted'):
        out[0] = 2
    elif simple.startswith('standardized'):
        out[0] = 1

    if simple.endswith('(l1)'):
        out[1] = 2
    elif simple.endswith('(l2)'):
        out[1] = 1

    return out

if __name__ == '__main__':
    import sys
    main(sys.argv[1:-1], sys.argv[-1])
