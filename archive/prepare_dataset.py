import data_io

import numpy as np

data_path = 'data/'
folds_path = 'folds/'

alignments = ['blits' + str(i) + '.' for i in range(2, 6)] + [''] + ['jackhmmer' + str(i) + '.' for i in range(4, 7)]
methods = ['psicov2', 'plmdca2']
combined_methods = [a + m for a in alignments for m in methods]

folds = 5

min_separation = 5

def prepare_dataset():
	total_pairs = 0
	fold_lengths = []
	for k in range(folds):
		fold_sequence_names = data_io.read_fold_sequence_names(folds_path, k + 1)
		fold_pairs = 0
		for sequence_name in fold_sequence_names:
			L = len(data_io.read_sequence(data_path, sequence_name))
			fold_pairs += (L - min_separation + 1) * (L - min_separation) / 2
		total_pairs += fold_pairs
		fold_lengths.append(fold_pairs)

	data = np.zeros((total_pairs, len(combined_methods)))
	target = np.zeros(total_pairs, dtype=np.int8)

	pairs = 0
	for k in range(folds):
		for sequence_name in data_io.read_fold_sequence_names(folds_path, k + 1):
			print sequence_name

			L = len(data_io.read_sequence(data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(data_path, sequence_name, L)

			for (c, method) in enumerate(combined_methods):
				r = pairs
				predictions, prediction_scores = data_io.read_predicted_contacts(data_path, sequence_name, L, method, 5)
				for i in range(L):
					for j in range(i + min_separation, L):
						data[r, c] = prediction_scores[i, j]
						if c == 0:
							target[r] = 0 < contact_matrix[i, j] <= 8
						r += 1
			pairs = r

	np.save('dataset_data.npy', data)
	np.save('dataset_target.npy', target)
	np.save('dataset_folds.npy', np.array([k for (k, n) in enumerate(fold_lengths) for j in range(n)]))

if __name__ == "__main__":
	prepare_dataset()
