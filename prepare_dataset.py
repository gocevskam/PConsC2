import constants
import data_io

import numpy as np

import collections
import math

number_of_extra_features = 1 + 2 * (len(constants.amino_acids) + 1) + 2 * (2 * constants.extra_features_window + 1) * 2 + 2 * (2 * constants.extra_features_window + 1) * 5
number_of_extra_same_ss_features = 3

def add_extra_features(data, sequence_name, L, row, column):
	alignment = data_io.read_alignment(constants.data_path, sequence_name)
	frequencies = [collections.defaultdict(int) for i in range(L)]
	for sequence in alignment:
		for i in range(L):
			frequencies[i][sequence[i]] += 1

	psipred_ss, psipred_conf = data_io.read_psipred(constants.data_path, sequence_name)
	netsurfp_rsa, netsurfp_ss = data_io.read_netsurfp(constants.data_path, sequence_name)

	r = row
	for i in range(L):
		for j in range(i + constants.min_separation, L):
			c = column
			
			# Separation
			data[r, c] = j - i
			c += 1

			# PSSM
			for k in (i, j):
				for (amino_acid, background_frequency) in zip(constants.amino_acids, constants.background_frequencies):
					data[r, c] = math.log((frequencies[k][amino_acid] if amino_acid in frequencies[k] else 0.01) / (len(alignment) * background_frequency))
					c += 1
				data[r, c] = math.log(frequencies[k]['-'] if '-' in frequencies[k] else 0.01) / float(len(alignment))
				c += 1

			# SS
			for k in (i, j):
				for l in range(k - constants.extra_features_window, k + constants.extra_features_window + 1):
					if 0 <= l < L:
						ss = constants.secondary_structures.index(psipred_ss[l])
						conf = psipred_conf[l]
					else:
						ss = -1
						conf = 0
					data[r, c:c+2] = (ss, conf)
					c += 2

			# RSA
			for k in (i, j):
				for l in range(k - constants.extra_features_window, k + constants.extra_features_window + 1):
					if 0 <= l < L:
						rsa = netsurfp_rsa[l]
						ss = netsurfp_ss[l]
					else:
						rsa = (0, -5)
						ss = (0, 0, 0)
					data[r, c:c+5] = rsa + ss
					c += 5

			r += 1

def add_extra_same_ss_features(data, sequence_name, L, row, column):
	psipred_ss, psipred_conf = data_io.read_psipred(constants.data_path, sequence_name)
	
	r = row
	for i in range(L):
		for j in range(i + constants.min_separation, L):
			c = column
			
			# Separation
			data[r, c] = j - i
			c += 1

			# Same SS element
			same_ss = psipred_ss[i] == psipred_ss[j] and psipred_ss[i] != 'C' and all(ss == psipred_ss[i] for ss in psipred_ss[i+1:j+1])
			same_ss_conf = min(psipred_conf[i:j+1]) if same_ss else 0
			data[r, c:c+2] = (same_ss, same_ss_conf)
			c += 2

		r += 1

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

	data = np.zeros((total_pairs, len(constants.combined_methods) * (9 if constants.surrounding_prediction_scores else 1) + constants.extra_features * number_of_extra_features + constants.extra_same_ss_features * number_of_extra_same_ss_features))
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

						if constants.surrounding_prediction_scores:
							cc = 1
							for u in range(i-1, i+2):
								for v in range(j-1, j+2):
									if u != i or v != j:
										data[r, cc * len(constants.combined_methods) + c] = prediction_scores[u, v] if (0 <= u < L and 0 <= v < L) else -10
										cc += 1
						r += 1

			if constants.extra_features:
				add_extra_features(data, sequence_name, L, pairs, len(constants.combined_methods))

			if constants.extra_same_ss_features:
				add_extra_same_ss_features(data, sequence_name, L, pairs, len(constants.combined_methods) + constants.extra_features * number_of_extra_features)

			pairs = r

	return data, target, folds

if __name__ == '__main__':
	data, target, folds = prepare_dataset()

	np.save(constants.intermediate_path + 'dataset_data.npy', data)
	np.save(constants.intermediate_path + 'dataset_target.npy', target)
	np.save(constants.intermediate_path + 'dataset_folds.npy', folds)
