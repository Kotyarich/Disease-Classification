import parser
import pickle
from sklearn import tree
import numpy as np
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.pipeline import FeatureUnion, make_pipeline


labels, data = parser.get_data()

fixed_l = []
fixed_d = []
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

fixed_d = np.array(fixed_d)
fixed_l = np.array(fixed_l)

transformer = FeatureUnion(transformer_list=[
    ('features', SimpleImputer(strategy='mean')),
    ('indicators', MissingIndicator())])

clf = make_pipeline(transformer, tree.DecisionTreeClassifier(max_depth=None,
                                                             max_features=22,
                                                             min_samples_leaf=3))

clf.fit(fixed_d, fixed_l)

file = open("model.skl",'wb')
pickle.dump(clf, file)
file.close()
