import itertools
import os
import re
import tarfile
import tempfile

import numpy as np

from sklearn.externals import joblib

split_re = re.compile(r'[, \t]+')

def read_sequence_names(data_path):
	with open(data_path + 'sequence_names', 'r') as f:
		return [l.strip() for l in f if l.strip()]

def read_fold_sequence_names(data_path, k):
	return read_sequence_names(data_path + 'folds/set' + str(k + 1))

def read_sequence(data_path, sequence_name):
	with open(data_path + 'sequences/' + sequence_name + '.fa', 'r') as f:
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
	for (i, j, c) in read_residue_pairs(data_path + 'contacts/' + sequence_name + '.CB', ' '):
		contacts[i-1, j-1] = c
		contacts[j-1, i-1] = c
	return contacts

def read_predicted_contacts(data_path, method, sequence_name, L, separation):
	predicted = []
	scores = np.zeros((L, L))
	for (i, j, s) in read_residue_pairs(data_path + method + '/' + sequence_name + '.pred', ',' if 'plmdca' in method else ' '):
		if abs(j - i) >= separation:
			predicted.append((i, j))
			scores[i-1, j-1] = s
			scores[j-1, i-1] = s
	predicted.sort(key=lambda (i, j): scores[i-1, j-1], reverse=True)
	return predicted, scores

def write_predictions(output_path, sequence_name, predicted):
	with open(output_path + sequence_name + '.pred', 'w') as f:
		predicted.sort(key=lambda (i, j, s): s, reverse=True)
		for (i, j, s) in predicted:
			f.write('{} {} {}\n'.format(i, j, s))

def save_random_forest(random_forest, output_path, file_name):
	for tree in random_forest.estimators_:
		tree.indices_ = None

	temp_dir = tempfile.gettempdir()
	temp_files = joblib.dump(random_forest, temp_dir + '/random_forest.pkl')

	with tarfile.open(output_path + file_name, 'w:gz') as tgz:
		for temp_file in temp_files:
			tgz.add(temp_file, arcname=os.path.basename(temp_file))

	for temp_file in temp_files:
		os.remove(temp_file)

def load_random_forest(input_path, file_name):
	temp_dir = tempfile.gettempdir()

	with tarfile.open(input_path + file_name, 'r') as tgz:
		tgz.extractall(temp_dir)

		random_forest = joblib.load(temp_dir + '/random_forest.pkl')

		for temp_file in tgz.getnames():
			os.remove(temp_dir + '/' + temp_file)

	return random_forest
