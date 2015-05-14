import constants
import data_io

import numpy as np

def prepare_dataset():
	total_pairs = 0
	fold_lengths = []
	for k in range(constants.number_of_folds):
		fold_sequence_names = data_io.read_fold_sequence_names(constants.data_path, k)
		fold_pairs = 0
		for sequence_name in fold_sequence_names:
			L = len(data_io.read_sequence(constants.data_path, sequence_name))
			fold_pairs += (L - constants.min_separation + 1) * (L - constants.min_separation) / 2
		total_pairs += fold_pairs
		fold_lengths.append(fold_pairs)

	data = np.zeros((total_pairs, len(constants.combined_methods)))
	target = np.zeros(total_pairs, dtype=np.int8)
	folds =  np.array([k for (k, n) in enumerate(fold_lengths) for j in range(n)])

	pairs = 0
	for k in range(constants.number_of_folds):
		for sequence_name in data_io.read_fold_sequence_names(constants.data_path, k):
			L = len(data_io.read_sequence(constants.data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(constants.data_path, sequence_name, L)

			for (c, method) in enumerate(constants.combined_methods):
				r = pairs
				predictions, prediction_scores = data_io.read_predicted_contacts(constants.data_path, method, sequence_name, L, constants.min_separation)
				for i in range(L):
					for j in range(i + constants.min_separation, L):
						data[r, c] = prediction_scores[i, j]
						if c == 0:
							target[r] = contact_matrix[i, j] <= 8 if contact_matrix[i, j] > 0 else -1
						r += 1
			pairs = r

	return data, target, folds

if __name__ == '__main__':
	data, target, folds = prepare_dataset()

	np.save(constants.intermediate_path + 'dataset_data.npy', data)
	np.save(constants.intermediate_path + 'dataset_target.npy', target)
	np.save(constants.intermediate_path + 'dataset_folds.npy', folds)
