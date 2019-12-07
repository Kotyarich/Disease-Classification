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
    ones = 0
    passed_ones = 0
    for i in range(len(expected)):
        result = clf.predict(data[i].reshape(1, -1))
        if result[0] == expected[i]:
            passed += 1
        if expected[i] == 1:
            ones += 1
            if result[0] == expected[i]:
                passed_ones += 1
    print('{}/{}; {}/{}'.format(passed_ones, ones, passed, len(expected)))
    return passed / len(expected)


def cross_validation(data, labels, max_depth, max_features, min_samples_leaf, od=[], ol=[]):
    data_sets, test_sets = get_test_and_teach_datas(data, labels)
    acc = 0
    for i in range(5):
        clf = teach_tree(np.array(data_sets[0][i]), np.array(data_sets[1][i]),
                         max_depth, max_features, min_samples_leaf)
        acc += get_accurance(clf, np.array(test_sets[0][i] + od), np.array(test_sets[1][i] + ol))
    acc = acc / 5 * 100
    print('{:.2f}: {}, {}, {}'.format(acc, max_depth, max_features, min_samples_leaf))
    return acc


def fix_data_set(data, labels):
    fixed_l = []
    fixed_d = []
    others_l = []
    others_d = []
    for i in range(len(labels)):
        if labels[i]:
            fixed_l.append(labels[i])
            fixed_d.append(data[i])

    l = int(len(fixed_l) / 1.3)
    count = 0
    for i in range(len(labels)):
        if not labels[i]:
            if count < l:
                count += 1
                fixed_l.append(labels[i])
                fixed_d.append(data[i])
            else:
                others_l.append(labels[i])
                others_d.append(data[i])

    return fixed_l, fixed_d, others_l, others_d


def main(labels, data):
    acc = 0
    params = ()
    for max_depth in [None] + [i for i in range(1, 50)]:
        for max_features in range(1, len(data[0]) + 1):
            for min_samples_leaf in range(1, 50):
                tmp_acc = cross_validation(data, labels, max_depth, max_features, min_samples_leaf)
                if tmp_acc > acc:
                    acc = tmp_acc
                    params = (max_depth, max_features, min_samples_leaf)
    print(acc)
    print(params[0], params[1], params[2])


if __name__ == '__main__':
    labels, data = parser.get_data()
    labels, data, not_teached_labels, not_teached_data = fix_data_set(data, labels)
    print(len(not_teached_labels))
    for md, mf, msl in ((None, 22, 3), (45, 33, 2)):
        _ = cross_validation(data, labels, md, mf, msl, not_teached_data, not_teached_labels)

# 45, 33, 2; 44, 3, 3, 42, 13, 2, 41, 21, 3, 38, 29, 3, 38, 26, 3, 38, 22, 2, 33, 30, 3, 32, 28, 2, None 22, 3
