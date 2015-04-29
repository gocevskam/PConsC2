import data_io

import numpy as np

from sklearn.externals import joblib

data_path = 'data/'
folds_path = 'folds/'
output_path = 'pconsc_predictions/'

data = np.load('dataset_data.npy')
folds = np.load('dataset_folds.npy')

min_separation = 5

for k in range(max(folds)+1):
	forest = joblib.load('forests/random_forest_' + str(k) + '.pkl')
	scores = forest.predict_proba(data[folds == k])

	r = 0
	fold_sequence_names = data_io.read_fold_sequence_names(folds_path, k + 1)
	for sequence_name in data_io.read_fold_sequence_names(folds_path, k + 1):
		predicted = []
		L = len(data_io.read_sequence(data_path, sequence_name))
		for i in range(L):
			for j in range(i + min_separation, L):
				predicted.append((i+1, j+1, scores[r]))
				r += 1
		data_io.write_predictions(output_path, sequence_name, predicted)