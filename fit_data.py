import constants as c
import data_io
import timer

import numpy as np
import sklearn.ensemble

def fit_data(k, data, target, folds):
	random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=100, min_samples_leaf=500, n_jobs=c.number_of_cores)
	random_forest_classifier.fit(data[folds != k], target[folds != k])
	return random_forest_classifier

if __name__ == '__main__':
	data = np.load(c.intermediate_path + 'dataset_data.npy')
	target = np.load(c.intermediate_path + 'dataset_target.npy')
	folds = np.load(c.intermediate_path + 'dataset_folds.npy')

	for k in range(c.number_of_folds):
		with timer.Timer() as t:
			random_forest = data_io.save_random_forest(fit_data(k, data, target, folds)
			data_io.save_random_forest(random_forest, c.intermediate_path, 'random_forest_' + str(k) + '.pkl.tar.gz')
		
		print k, "{:10.3f}".format(t.secs)
