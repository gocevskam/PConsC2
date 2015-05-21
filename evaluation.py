import constants
import data_io

import matplotlib.pyplot as plt

import cPickle as pickle
import itertools

grouped_methods_layers = [
	('psicov', (constants.data_path, [a + '_' + 'psicov' for a in constants.alignments], 'PSICOV', 'k')),
	('plmdca', (constants.data_path, [a + '_' + 'plmdca' for a in constants.alignments], 'plmDCA', 'g')),
	('pconsc', (constants.results_path, ['no_extra/pconsc2_layer_0'], 'PconsC', 'r')),
	('pconsc2_layer_1', (constants.results_path, ['no_extra/pconsc2_layer_1'], 'Layer 1', '#99C2FF')),
	('pconsc2_layer_2', (constants.results_path, ['no_extra/pconsc2_layer_2'], 'Layer 2', '#80B2FF')),
	('pconsc2_layer_3', (constants.results_path, ['no_extra/pconsc2_layer_3'], 'Layer 3', '#66A3FF')),
	('pconsc2_layer_4', (constants.results_path, ['no_extra/pconsc2_layer_4'], 'Layer 4', '#3385FF')),
	('pconsc2_layer_5', (constants.results_path, ['no_extra/pconsc2_layer_5'], 'PconsC2', '#005CE6')),
]

grouped_methods_extra = [
	('psicov', (constants.data_path, [a + '_' + 'psicov' for a in constants.alignments], 'PSICOV', 'k')),
	('plmdca', (constants.data_path, [a + '_' + 'plmdca' for a in constants.alignments], 'plmDCA', 'g')),
	('pconsc', (constants.results_path, ['no_extra/pconsc2_layer_0'], 'PconsC', 'r')),
	('pconsc2_layer_5', (constants.results_path, ['no_extra/pconsc2_layer_5'], 'PconsC2', '#005CE6')),
	('pconsc_extra', (constants.results_path, ['extra/pconsc2_layer_0'], 'PconsC (extra features)', 'orange')),
	('pconsc2_layer_5_extra', (constants.results_path, ['extra/pconsc2_layer_5'], 'PconsC2 (extra features)', '#9966FF')),
]

grouped_methods_ss = [
	('psicov', (constants.data_path, [a + '_' + 'psicov' for a in constants.alignments], 'PSICOV', 'k')),
	('plmdca', (constants.data_path, [a + '_' + 'plmdca' for a in constants.alignments], 'plmDCA', 'g')),
	('pconsc', (constants.results_path, ['no_extra/pconsc2_layer_0'], 'PconsC', 'r')),
	('pconsc2_layer_5', (constants.results_path, ['no_extra/pconsc2_layer_5'], 'PconsC2', '#005CE6')),
	('pconsc_ss', (constants.results_path, ['no_extra_same_ss/pconsc2_layer_0'], 'PconsC (SS features)', '#993300')),
	('pconsc2_layer_5_ss', (constants.results_path, ['no_extra_same_ss/pconsc2_layer_5'], 'PconsC2 (SS features)', '#009999')),
]

grouped_methods_surrounding = [
	('psicov', (constants.data_path, [a + '_' + 'psicov' for a in constants.alignments], 'PSICOV', 'k')),
	('plmdca', (constants.data_path, [a + '_' + 'plmdca' for a in constants.alignments], 'plmDCA', 'g')),
	('pconsc', (constants.results_path, ['no_extra/pconsc2_layer_0'], 'PconsC', 'r')),
	('pconsc2_layer_1', (constants.results_path, ['no_extra/pconsc2_layer_1'], 'Layer 1', '#99C2FF')),
	('pconsc2_layer_5', (constants.results_path, ['no_extra/pconsc2_layer_5'], 'PconsC2', '#005CE6')),
	('pconsc_surrounding', (constants.results_path, ['surrounding/pconsc2_layer_0'], 'PconsC (surrounding scores)', '#993300')),
	('pconsc2_layer_1_surrounding', (constants.results_path, ['surrounding/pconsc2_layer_1'], 'Layer 1 (surrounding scores)', '#99D6D6')),
	('pconsc2_layer_5_surrounding', (constants.results_path, ['surrounding/pconsc2_layer_5'], 'PconsC2 (surrounding scores)', '#009999')),
]

grouped_methods = grouped_methods_layers

def average_ppv(method):
	top_predictions_fraction = 1.0

	sequence_names = data_io.read_sequence_names(constants.data_path)
	ppv = []
	for sequence_name in sequence_names:
		L = len(data_io.read_sequence(constants.data_path, sequence_name))
		contact_matrix = data_io.read_contacts_matrix(constants.data_path, sequence_name, L)
		predictions, prediction_scores = data_io.read_predicted_contacts(constants.results_path, method, sequence_name, L, 5)
		predictions = [(i, j) for (i, j) in predictions if contact_matrix[i-1,j-1] > 0]
		predictions = predictions[:int(top_predictions_fraction * L)]
		if len(predictions) > 0:
			ppv.append(sum(1 for (i, j) in predictions if contact_matrix[i-1,j-1] <= 8) / float(len(predictions)))
			print sequence_name, L, ppv[-1]
		else:
			print sequence_name, L, "No predictions"
	print 'Average PPV:', sum(ppv) / len(ppv)

def plot_ppv():
	max_predictions_fraction = 2.0

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
					predictions = [(i, j) for (i, j) in predictions if contact_matrix[i-1,j-1] > 0]
					predictions = predictions[:int(max_predictions_fraction * L)]
					all_predictions[grouped_method].extend((100 * float(k) / L, contact_matrix[i-1,j-1] <= 8) for (k, (i, j)) in enumerate(predictions, 1))

		return all_predictions

	def accumulate_predictions(predictions):
		ppv = {}

		for (grouped_method, _) in grouped_methods:
			predictions[grouped_method].sort()

			k = 0
			n = 0
			X = []
			Y = []
			for x, prediction_list in itertools.groupby(predictions[grouped_method], key=lambda x: x[0]):
				prediction_list = list(prediction_list)
				k += sum(1 for p in prediction_list if p[1])
				n += len(prediction_list)
				if x >= 1:
					X.append(x)
					Y.append(float(k) / n)
			ppv[grouped_method] = (X, Y)

		return ppv

	def plot_ppv_curves(ppv):
		for (grouped_method, (base_path, methods, name, style)) in grouped_methods:
			X, Y = ppv[grouped_method]
			plt.plot(X, Y, style, label=name)
		plt.legend(ncol=2)
		plt.xlabel('Maximum relative rank of contacts (%)')
		plt.ylabel('PPV')
		plt.xlim([0, 100 * max_predictions_fraction])
		plt.show()

	predictions = get_all_predictions()
	ppv = accumulate_predictions(predictions)

	for (grouped_method, (base_path, methods, name, style)) in grouped_methods:
		print name, next(y for (x, y) in zip(*ppv[grouped_method]) if x >= 100)

	plot_ppv_curves(ppv)

if __name__ == "__main__":
	#average_ppv('no_extra/pconsc2_layer_0')
	plot_ppv()
