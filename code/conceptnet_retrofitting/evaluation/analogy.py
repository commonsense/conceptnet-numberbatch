from conceptnet_retrofitting import loaders
from conceptnet_retrofitting.word_vectors import WordVectors
from conceptnet_retrofitting.builders.label_set import LabelSet
from conceptnet_retrofitting.builders.build_assoc import build_relations_from_conceptnet
import numpy as np
import argparse


def which_relation(wv, rel_array, c1, c2):
    """
    Infer what relation or relations are likely to exist between
    c1 and c2.

    Returns a vector of squared relation strengths, whose length is the number
    of relations and whose sum is 1.
    """
    any_rel = np.mean(wv.vectors, 0) @ rel_array @ np.mean(wv.vectors, 0)
    rels = wv.to_vector(c2) @ rel_array @ wv.to_vector(c1)
    diff = np.maximum(0, rels - any_rel) ** 2
    diffsum = np.sum(diff)
    if diffsum > 0:
        diff /= diffsum
    return diff


def rank3_inner_product(vec, array3):
    """
    Compute the inner product of a vector and a rank-3 array, with the
    product taken along axis 0. The result is a matrix shaped like
    axes 1 and 2 of the array.
    """
    return (array3 * vec[:, np.newaxis, np.newaxis]).sum(0)


def eval_analogy(wv, rel_array, c1, c2, c3, c4, power=2):
    """
    Evaluate the strength of an analogy between c1, c2, c3, and c4.
    Comparing these results can provide an answer to a multiple-choice analogy
    question.

    `wv` is the WordVectors object to look up words in. `rel_array` is the
    rank-3 array of how each relation relates vectors to other vectors.
    `power` is how much to emphasize the relations between (c1, c2) and
    (c3, c4), as opposed to those between (c1, c3) and (c2, c4).
    """
    if c4 in (c1, c2, c3):
        return 0.
    try:
        relA = which_relation(wv, rel_array, c1, c2)
        relB = which_relation(wv, rel_array, c1, c3)
        relAr = rank3_inner_product(relA, rel_array)
        relBr = rank3_inner_product(relB, rel_array)
        v1, v2, v3, v4 = [wv.to_vector(c) for c in (c1, c2, c3, c4)]
        numer1 = v4 @ relAr @ v3 + 1
        numer2 = v4 @ relBr @ v2 + 1
        denom1 = v4 @ relAr @ v1 + 1
        denom2 = v4 @ relBr @ v1 + 1
    except KeyError:
        return 0.
    return (numer1 ** power * numer2) / (denom1 + denom2)


def eval_analogy_modified_3cosmul(wv, c1, c2, c3, c4, power=2):
    """
    Evaluate the strength of an analogy using modified 3cosmul (where the
    relationship between c3 and c4 is more important than that between
    c2 and c4).

    This is an effective way to compute analogies over vectors that does
    not require any information about relations.
    """
    try:
        v4 = wv.to_vector(c4)
        sim1 = v4 @ wv.to_vector(c1) + 1.000001
        sim2 = v4 @ wv.to_vector(c2) + 1
        sim3 = v4 @ wv.to_vector(c3) + 1
    except KeyError:
        return 0.
    return sim2 * (sim3 ** power) / sim1


def analogy(wv, rel_array, c1, c2, c3, num=20, power=2, verbose=True):
    """
    Rank term by how well they fit an analogy, as in `eval_analogy`.
    The best `num` terms and their scores will be returned.

    The inferred relations between (c1, c2) and (c1, c3) will be
    displayed if verbose is True.
    """
    relA = which_relation(wv, rel_array, c1, c2)
    relB = which_relation(wv, rel_array, c1, c3)
    if verbose:
        print("RelA")
        for label, strength in zip(rel_labels + rel_labels, relA):
            print('\t%-20s\t% 7.1f' % (label, strength * 1000))
        print("RelB")
        for label, strength in zip(rel_labels + rel_labels, relB):
            print('\t%-20s\t% 7.1f' % (label, strength * 1000))
    relAr = rank3_inner_product(relA, rel_array)
    relBr = rank3_inner_product(relB, rel_array)
    v1, v2, v3 = [wv.to_vector(c) for c in (c1, c2, c3)]
    numer1 = wv.vectors @ (relAr @ v3) + 1
    numer2 = wv.vectors @ (relBr @ v2) + 1
    denom1 = wv.vectors @ (relAr @ v1) + 1
    denom2 = wv.vectors @ (relBr @ v1) + 1
    ratings = (numer1 ** power * numer2) / (denom1 + denom2)
    sortorder = np.argsort(-ratings)
    found = []
    for idx in sortorder:
        label = wv.labels[idx]
        if en_filter(label):
            found.append((label, ratings[idx]))
        if len(found) >= num:
            break
    return found


def read_analogies(filename):
    for line in open(filename, encoding='utf-8'):
        line = line.rstrip()
        if not line or line.startswith('#'):
            continue
        parts = line.split('\t')
        inputs = parts[1:4]
        answers = parts[4:]
        yield inputs, answers


def eval_analogies(analogy_func, filename='/nfs/broadway/data/corpora/readtheory-analogies.txt'):
    total = 0
    correct = 0
    for inputs, answers in read_analogies(filename):
        # The 'inputs' are the three given components of the analogy.
        # 'answers' are the multiple-choice answers, where the correct answer is first in the list.
        best_score = 0.
        best_answer = ''
        for answer in answers:
            quad = inputs + [answer]
            score = analogy_func(*quad)
            if score >= best_score:
                best_score = score
                best_answer = answer
        total += 1
        if best_answer == answers[0]:
            correct += 1
        else:
            items = tuple(inputs + [best_answer.upper()] + [answers[0].upper()])
            print("%s : %s :: %s : %s (should be %s)" % items)
    print("Score: %2.2f%% (%d/%d)" % (correct / total * 100, correct, total))
    return correct / total


def make_dense_relation_array(wv, sparse_rels, endrow=100000):
    rel_array = loaders.dense_relation_array(
        wv.vectors[:endrow],
        {rel: sp[:endrow, :endrow] for (rel, sp) in sparse_rels.items()}
    )
    return rel_array


def main(labels_in, vecs_in, replacements_in, sparse_relations_in, analogy_file, verbose=True):
    wv = loaders.load_word_vectors(labels_in, vecs_in, replacements_in)
    labels = LabelSet(wv.labels)
    if sparse_relations_in is not None:
        sparse_rels = build_relations_from_conceptnet(labels, sparse_relations_in)
        rel_array = make_dense_relation_array(wv, sparse_rels)
    else:
        rel_array = sparse_rels = None
    
    def analogy_func(c1, c2, c3, c4):
        if sparse_rels is None:
            return eval_analogy_modified_3cosmul(wv, c1, c2, c3, c4)
        else:
            return eval_analogy(wv, rel_array, c1, c2, c3, c4)

    return eval_analogies(analogy_func, analogy_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('labels')
    parser.add_argument('vectors')
    parser.add_argument('-r', '--replacements', default=None)
    parser.add_argument('-s', '--sparse-rels', default=None, help='The file of sparse relational knowledge to learn from')
    parser.add_argument('-a', '--analogies', default='/nfs/broadway/data/corpora/readtheory-analogies.txt', help='The file of multiple-choice analogies to evaluate')
    args = parser.parse_args()
    main(args.labels, args.vectors, args.replacements, args.sparse_rels, args.analogies)

