import constants as c
import data_io

import numpy as np
from sklearn.externals import joblib

def predict_data(k, data, folds, random_forest):
	scores = random_forest.predict_proba(data[folds == k])[:, where(random_forest.classes_ == 1)[0]]

	r = 0
	fold_sequence_names = data_io.read_fold_sequence_names(c.data_path, k)
	for sequence_name in fold_sequence_names:
		predicted = []
		L = len(data_io.read_sequence(c.data_path, sequence_name))
		for i in range(L):
			for j in range(i + c.min_separation, L):
				predicted.append((i+1, j+1, scores[r]))
				r += 1
		data_io.write_predictions(c.results_path + 'pconsc/', sequence_name, predicted)

if __name__ == '__main__':
	data = np.load(c.intermediate_path + 'dataset_data.npy')
	folds = np.load(c.intermediate_path + 'dataset_folds.npy')

	for k in range(c.number_of_folds):
		random_forest = data_io.load_random_forest(c.intermediate_path, 'random_forest_' + str(k) + '.pkl.tar.gz')
		predict_data(k, data, folds, random_forest)
