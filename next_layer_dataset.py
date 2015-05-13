import constants
import data_io

import numpy as np

def previous_layer_predictions(scores, L, row):
	predictions = np.zeros((L, L))
	for i in range(L):
		for j in range(i + constants.min_separation, L):
			predictions[i, j] = scores[row]
			row += 1
	return predictions

def next_layer_dataset(base_data, previous_data, previous_forest):
	data = np.zeros((base_data.shape[0], base_data.shape[1] + (2 * constants.receptive_field + 1) ** 2))
	data[:,:base_data.shape[1]] = base_data

	scores = previous_forest.predict_proba(previous_data)[:, np.where(previous_forest.classes_ == 1)[0][0]]
	r = 0
	for k in range(constants.number_of_folds):
		for sequence_name in data_io.read_fold_sequence_names(constants.data_path, k):
			L = len(data_io.read_sequence(constants.data_path, sequence_name))
			previous_predictions = previous_layer_predictions(scores, L, r)
			for i in range(L):
				for j in range(i + constants.min_separation, L):
					c = base_data.shape[1]
					for u in range(i - constants.receptive_field, i + constants.receptive_field + 1):
						for v in range(j - constants.receptive_field, j + constants.receptive_field + 1):
							if 0 <= u < L and 0 <= v < L:
								data[r, c] = previous_predictions[u, v]
							c += 1
					r += 1

	return data

if __name__ == '__main__':
	k = 0
	l = 1

	base_data = np.load(constants.intermediate_path + 'dataset_data.npy')
	if l == 1:
		previous_data = np.load(constants.intermediate_path + 'dataset_data.npy')
		previous_forest = data_io.load_random_forest(constants.intermediate_path, 'random_forest_' + str(k) + '.pkl.tar.gz')
	else:
		previous_data = np.load(constants.intermediate_path + 'dataset_data_' + str(k) + '_layer_' + str(l-1) + '.npy')
		previous_forest = data_io.load_random_forest(constants.intermediate_path, 'random_forest_' + str(k) + '_layer_' + str(l-1) + '.pkl.tar.gz')

	data = next_layer_dataset(base_data, previous_data, previous_forest)
	
	np.save(constants.intermediate_path + 'dataset_data_' + str(k) + '_layer_' + str(l) + '.npy', data)
