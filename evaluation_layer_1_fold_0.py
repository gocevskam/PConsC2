import constants as c
import data_io

import matplotlib.pyplot as plt

import cPickle as pickle
import itertools

grouped_methods = [
	('psicov', (c.data_path, [a + '_' + 'psicov' for a in c.alignments], 'PSICOV', 'k:')),
	('plmdca', (c.data_path, [a + '_' + 'plmdca' for a in c.alignments], 'plmDCA', 'g--')),
	('pconsc', (c.results_path, ['pconsc'], 'PconsC', 'r-')),
	('pconsc2_layer_1', (c.results_path, ['pconsc2_layer_1'], 'PconsC2 Layer 1', 'b-')),
]

def average_ppv(method):
	top_predictions_fraction = 1.0

	sequence_names = data_io.read_sequence_names(c.data_path)
	ppv = []
	for sequence_name in sequence_names:
		L = len(data_io.read_sequence(c.data_path, sequence_name))
		contact_matrix = data_io.read_contacts_matrix(c.data_path, sequence_name, L)
		predictions, prediction_scores = data_io.read_predicted_contacts(c.data_path, method, sequence_name, L, 5)
		predictions = predictions[:int(top_predictions_fraction * L)]
		if len(predictions) > 0:
			ppv.append(sum(1 for (i, j) in predictions if 0 < contact_matrix[i-1,j-1] <= 8) / float(len(predictions)))
			print sequence_name, L, ppv[-1]
		else:
			print sequence_name, L, "No predictions"
	print 'Average PPV:', sum(ppv) / len(ppv)

def plot_ppv():
	max_predictions_fraction = 2.0

	def get_all_predictions():
		sequence_names = data_io.read_fold_sequence_names(c.data_path, 0)

		all_predictions = dict((grouped_method, []) for (grouped_method, _) in grouped_methods)

		for sequence_name in sequence_names:
			print sequence_name

			L = len(data_io.read_sequence(c.data_path, sequence_name))
			contact_matrix = data_io.read_contacts_matrix(c.data_path, sequence_name, L)

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

	try:
		predictions = pickle.load(open(c.intermediate_path + 'evaluation_predictions.pickled', 'rb'))
	except:
		predictions = get_all_predictions()
		pickle.dump(predictions, open(c.intermediate_path + 'evaluation_predictions.pickled', 'wb'))

	try:
		ppv = pickle.load(open(c.intermediate_path + 'evaluation_ppv.pickled', 'rb'))
	except:
		ppv = accumulate_predictions(predictions)
		pickle.dump(ppv, open(c.intermediate_path + 'evaluation_ppv.pickled', 'wb'))

	plot_ppv_curves(ppv)

if __name__ == "__main__":
	#average_ppv('hhblits_1_psicov')
	plot_ppv()
