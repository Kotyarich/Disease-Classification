# from sklearn import tree
import numpy as np
import parser

labels, data = parser.get_data()
np_labels = np.array(labels)
np_data = np.array(data, ndmin=2)
print(np_data[0])

