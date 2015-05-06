import constants as c
import data_io
import timer

import numpy as np
import sklearn.ensemble

data = np.load(c.intermediate_path + 'dataset_data.npy')
target = np.load(c.intermediate_path + 'dataset_target.npy')
folds = np.load(c.intermediate_path + 'dataset_folds.npy')

"""for n in (100, 1000, 10000, 100000, 1000000, len(target)):
	with timer.Timer() as t:
		random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=20, min_samples_leaf=50, n_jobs=4)
		random_forest_classifier.fit(data[:n], target[:n])

	print "{:7}".format(n), "{:10.3f}".format(t.secs), t.secs / n"""

for k in range(max(folds)+1):
	with timer.Timer() as t:
		random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=100, min_samples_leaf=500, n_jobs=c.number_of_cores)
		random_forest_classifier.fit(data[folds != k], target[folds != k])

		data_io.save_random_forest(random_forest_classifier, c.intermediate_path, 'random_forest_' + str(k) + '.pkl.tar.gz')

	print k, "{:10.3f}".format(t.secs)
