import constants as c
import data_io

import numpy as np

def previous_layer_predictions(scores, L, row):
	predictions = np.zeros((L, L))
	for i in range(L):
		for j in range(i + c.min_separation, L):
			predictions[i, j] = scores[row]
			row += 1
	return predictions

def prepare_dataset(fold):
	total_pairs = 0
	fold_lengths = []
	for k in range(c.number_of_folds):
		fold_sequence_names = data_io.read_fold_sequence_names(c.data_path, k)
		fold_pairs = 0
		for sequence_name in fold_sequence_names:
			L = len(data_io.read_sequence(c.data_path, sequence_name))
			fold_pairs += (L - c.min_separation + 1) * (L - c.min_separation) / 2
		total_pairs += fold_pairs
		fold_lengths.append(fold_pairs)

	data = np.zeros((total_pairs, len(c.combined_methods) + (2 * c.receptive_field + 1) ** 2))

	pairs = 0
	for k in range(c.number_of_folds):
		for sequence_name in data_io.read_fold_sequence_names(c.data_path, k):
			print sequence_name

			L = len(data_io.read_sequence(c.data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(c.data_path, sequence_name, L)

			for (c, method) in enumerate(c.combined_methods):
				r = pairs
				predictions, prediction_scores = data_io.read_predicted_contacts(c.data_path, method, sequence_name, L, c.min_separation)
				for i in range(L):
					for j in range(i + c.min_separation, L):
						data[r, c] = prediction_scores[i, j]
						r += 1
			pairs = r

	forest = data_io.load_random_forest(c.intermediate_path, 'random_forest_' + str(fold) + '.pkl.tar.gz')
	prev_data = np.load(c.intermediate_path + 'dataset_data.npy')
	scores = forest.predict_proba(prev_data)[:, forest.classes_ == 1]
	r = 0
	for k in range(c.number_of_folds):
		for sequence_name in data_io.read_fold_sequence_names(c.data_path, k):
			L = len(data_io.read_sequence(c.data_path, sequence_name))
			prev_predictions = previous_layer_predictions(scores, L, r)
			for i in range(L):
				for j in range(i + c.min_separation, L):
					c = len(c.combined_methods)
					for u in range(i - c.receptive_field, i + c.receptive_field + 1):
						for v in range(j - c.receptive_field, j + c.receptive_field + 1):
							if 0 <= u < L and 0 <= v < L:
								data[r, c] = prev_predictions[u, v]
							c += 1
					r += 1

	np.save(c.intermediate_path + 'dataset_data_' + str(fold) + '_layer_1.npy', data)

if __name__ == "__main__":
	prepare_dataset(0)