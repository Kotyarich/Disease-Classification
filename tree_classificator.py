from sklearn import tree
import numpy as np
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.pipeline import FeatureUnion, make_pipeline

import parser


def get_test_and_teach_datas(data, labels):
    data_sets = []
    labels_sets = []
    test_data_sets = []
    test_labels_sets = []

    offset = int(len(labels) / 5)
    start_offset = 0
    for i in range(5):
        test_data_sets.append(data[start_offset:start_offset + offset])
        test_labels_sets.append(labels[start_offset:start_offset + offset])

        data_sets.append(data[:start_offset] + data[start_offset + offset:])
        labels_sets.append(labels[:start_offset] + labels[start_offset + offset:])

        start_offset += offset

    return (data_sets, labels_sets), (test_data_sets, test_labels_sets)


def teach_tree(data, labels, max_depth, max_features, min_samples_leaf):
    transformer = FeatureUnion(
        transformer_list=[
            ('features', SimpleImputer(strategy='mean')),
            ('indicators', MissingIndicator())])
    clf = make_pipeline(transformer, tree.DecisionTreeClassifier(
        max_depth=max_depth,
        max_features=max_features,
        min_samples_leaf=min_samples_leaf))
    clf.fit(data, labels)
    return clf


def get_accurance(clf, data, expected):
    passed = 0
    for i in range(len(expected)):
        result = clf.predict(data[i].reshape(1, -1))
        if result[0] == expected[i]:
            passed += 1
    return passed / len(expected)


def cross_validation(data, labels, max_depth, max_features, min_samples_leaf):
    data_sets, test_sets = get_test_and_teach_datas(data, labels)
    acc = 0
    for i in range(5):
        clf = teach_tree(np.array(data_sets[0][i]), np.array(data_sets[1][i]),
                         max_depth, max_features, min_samples_leaf)
        acc += get_accurance(clf, np.array(test_sets[0][i]), np.array(test_sets[1][i]))
    acc = acc / 5 * 100
    print('{:.2f}: {}, {}, {}'.format(acc, max_depth, max_features, min_samples_leaf))


if __name__ == '__main__':
    labels, data = parser.get_data()
    for max_depth in [None] + [i for i in range(1, 50)]:
        for max_features in range(1, len(data[0]) + 1):
            for min_samples_leaf in range(1, 50):
                cross_validation(data, labels, max_depth, max_features, min_samples_leaf)
