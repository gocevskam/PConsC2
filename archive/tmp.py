import numpy as np
import sklearn.ensemble

from sklearn.externals import joblib

import timer

n_jobs = -1

data = np.load('dataset_data.npy')
target = np.load('dataset_target.npy')
folds = np.load('dataset_folds.npy')

"""for n in (100, 1000, 10000, 100000, 1000000, len(target)):
	with timer.Timer() as t:
		random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=20, min_samples_leaf=50, n_jobs=4)
		random_forest_classifier.fit(data[:n], target[:n])

		joblib.dump(random_forest_classifier, 'forests/rfc_' + str(n) + '.pkl') 

	print "{:7}".format(n), "{:10.3f}".format(t.secs), t.secs / n"""

for k in range(max(folds)+1):
	with timer.Timer() as t:
		random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=100, min_samples_leaf=50, n_jobs=n_jobs)
		random_forest_classifier.fit(data[folds != k], target[folds != k])
		
		joblib.dump(random_forest_classifier, 'forests/random_forest_' + str(k) + '.pkl')

	print k, "{:10.3f}".format(t.secs)
