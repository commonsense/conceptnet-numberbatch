from conceptnet5.nodes import standardized_concept_uri

def standardize_vecs(labels, vecs):
    standardize_labels = []
    labels_to_index = {}
    standardized_vecs = []

    for index, (label, vec) in enumerate(zip(labels, vecs)):
        try:
            standardize_label = standardized_concept_uri('en', label)
        except ValueError:
            continue

        vec = vec / (index + 1)

        if concept not in labels_to_index:
            standardize_labels.append(standardize_label)
            labels_to_index[standardize_label] = index
            standardized_vecs.append(vec)
        else:
            index = labels_to_index[standardize_label]
            standardize_vecs[index] += vec

    return standardize_labels, standardize_vecs
