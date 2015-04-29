import itertools
import re

import numpy as np

split_re = re.compile(r'[, \t]+')

def read_sequence_names(file_name):
	with open(file_name, 'r') as f:
		return [l.strip() for l in f if l.strip()]

def read_fold_sequence_names(folds_path, k):
	return read_sequence_names(folds_path + 'set' + str(k))

def read_sequence(data_path, sequence_name):
	with open(data_path + sequence_name + '/sequence.fa', 'r') as f:
		for line in f:
			line = line.strip()
			if not line.startswith('>'):
				return line

def read_residue_pairs(file_name, separator):
	with open(file_name, 'r') as f:
		for line in f:
			line = line.strip()
			if line:
				splitted = line.split(separator)
				i = int(splitted[0])
				j = int(splitted[1])
				v = float(splitted[-1])
				yield (i, j, v)

def read_contacts_matrix(data_path, sequence_name, L):
	contacts = np.zeros((L, L))
	for (i, j, c) in read_residue_pairs(data_path + sequence_name + '/contacts.CB', ' '):
		contacts[i-1, j-1] = c
		contacts[j-1, i-1] = c
	return contacts

def read_predicted_contacts(data_path, sequence_name, L, method, separation):
	predicted = []
	scores = np.zeros((L, L))
	for (i, j, s) in read_residue_pairs(data_path + sequence_name + '/sequence.fa.' + method, ',' if 'plmdca' in method else ' '):
		if abs(j - i) >= separation:
			predicted.append((i, j))
			scores[i-1, j-1] = s
			scores[j-1, i-1] = s
	predicted.sort(key=lambda (i, j): scores[i-1, j-1], reverse=True)
	return predicted, scores

def write_predictions(output_path, sequence_name, predicted):
	with open(output_path + sequence_name, 'w') as f:
		predicted.sort(key=lambda (i, j, s): s, reverse=True)
		for (i, j, s) in predicted:
			f.write('{} {} {}\n'.format(i, j, s))
