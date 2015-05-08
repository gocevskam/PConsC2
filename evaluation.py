import constants
import data_io

import matplotlib.pyplot as plt

import cPickle as pickle
import itertools

grouped_methods = [
	('psicov', (constants.data_path, [a + '_' + 'psicov' for a in constants.alignments], 'PSICOV', 'k:')),
	('plmdca', (constants.data_path, [a + '_' + 'plmdca' for a in constants.alignments], 'plmDCA', 'g--')),
	('pconsc', (constants.results_path, ['pconsc'], 'PconsC', 'r-')),
]

def average_ppv(method):
	top_predictions_fraction = 1.0

	sequence_names = data_io.read_sequence_names(constants.data_path)
	ppv = []
	for sequence_name in sequence_names:
		L = len(data_io.read_sequence(constants.data_path, sequence_name))
		contact_matrix = data_io.read_contacts_matrix(constants.data_path, sequence_name, L)
		predictions, prediction_scores = data_io.read_predicted_contacts(constants.data_path, method, sequence_name, L, 5)
		predictions = predictions[:int(top_predictions_fraction * L)]
		if len(predictions) > 0:
			ppv.append(sum(1 for (i, j) in predictions if 0 < contact_matrix[i-1,j-1] <= 8) / float(len(predictions)))
			print sequence_name, L, ppv[-1]
		else:
			print sequence_name, L, "No predictions"
	print 'Average PPV:', sum(ppv) / len(ppv)

def plot_ppv():
	max_predictions_fraction = 1.5

	def get_all_predictions():
		sequence_names = data_io.read_sequence_names(constants.data_path)

		all_predictions = dict((grouped_method, []) for (grouped_method, _) in grouped_methods)

		for sequence_name in sequence_names:
			print sequence_name

			L = len(data_io.read_sequence(constants.data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(constants.data_path, sequence_name, L)

			for (grouped_method, (base_path, methods, name, style)) in grouped_methods:
				for method in methods:
					predictions, prediction_scores = data_io.read_predicted_contacts(base_path, method, sequence_name, L, 5)
					predictions = predictions[:int(max_predictions_fraction * L)]
					all_predictions[grouped_method].extend((100 * float(k) / L, 0 < contact_matrix[i-1,j-1] <= 8) for (k, (i, j)) in enumerate(predictions))

		return all_predictions

	def accumulate_predictions(predictions):
		ppv = {}

		for (grouped_method, _) in grouped_methods:
			predictions[grouped_method].sort()

			k = 0
			n = 0
			X = [0.0]
			Y = [0.0]
			for x, prediction_list in itertools.groupby(predictions[grouped_method], key=lambda x: x[0]):
				prediction_list = list(prediction_list)
				k += sum(1 for p in prediction_list if p[1])
				n += len(prediction_list)
				X.append(x)
				Y.append(float(k) / n)
			ppv[grouped_method] = (X, Y)

		return ppv

	def plot_ppv_curves(ppv):
		for (grouped_method, (base_path, methods, name, style)) in grouped_methods:
			X, Y = ppv[grouped_method]
			plt.plot(X, Y, style, label=name)
		plt.legend()
		plt.show()

	predictions = get_all_predictions()
	ppv = accumulate_predictions(predictions)
	plot_ppv_curves(ppv)

if __name__ == "__main__":
	#average_ppv('hhblits_1_psicov')
	plot_ppv()
