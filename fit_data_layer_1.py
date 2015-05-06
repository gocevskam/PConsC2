from constants import *
import data_io
import timer

import numpy as np
import sklearn.ensemble

n_jobs = -1

data = np.load(intermediate_path + 'dataset_data_0_layer_1.npy')
target = np.load(intermediate_path + 'dataset_target.npy')
folds = np.load(intermediate_path + 'dataset_folds.npy')

"""for n in (100, 1000, 10000, 100000, 1000000, len(target)):
	with timer.Timer() as t:
		random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=20, min_samples_leaf=50, n_jobs=4)
		random_forest_classifier.fit(data[:n], target[:n])

	print "{:7}".format(n), "{:10.3f}".format(t.secs), t.secs / n"""

k = 0
with timer.Timer() as t:
	random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=100, min_samples_leaf=500, n_jobs=n_jobs)
	random_forest_classifier.fit(data[folds != k], target[folds != k])

	data_io.save_random_forest(random_forest_classifier, intermediate_path, 'random_forest_' + str(k) + '_layer_1.pkl.tar.gz')

print k, "{:10.3f}".format(t.secs)