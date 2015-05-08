import constants
import data_io
import timer

import numpy as np
import sklearn.ensemble

def fit_data(k, data, target, folds):
	random_forest_classifier = sklearn.ensemble.RandomForestClassifier(n_estimators=100, min_samples_leaf=500, n_jobs=constants.number_of_cores)
	random_forest_classifier.fit(data[folds != k], target[folds != k])
	return random_forest_classifier

if __name__ == '__main__':
	data = np.load(constants.intermediate_path + 'dataset_data.npy')
	target = np.load(constants.intermediate_path + 'dataset_target.npy')
	folds = np.load(constants.intermediate_path + 'dataset_folds.npy')

	for k in range(constants.number_of_folds):
		with timer.Timer() as t:
			random_forest = fit_data(k, data, target, folds)
			data_io.save_random_forest(random_forest, constants.intermediate_path, 'random_forest_' + str(k) + '.pkl.tar.gz')

		print k, "{:10.3f}".format(t.secs)
