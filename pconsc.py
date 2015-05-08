import constants as c
import prepare_dataset
import data_io

import argparse
import os.path
import sys

def run_pconsc(fold_k):
	data, target, folds = prepare_dataset.prepare_dataset()
	forest = fit_data.fit_data(fold_k, data, target, folds)
	data_io.save_random_forest(forest, c.intermediate_path, 'pconsc_random_forest_' + str(k) + '.pkl.tar.gz')
	predict_data.predict_data(fold_k, data, folds, forest)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run PConsC')
	parser.add_argument('-d', '--data')
	parser.add_argument('-i', '--intermediate')
	parser.add_argument('-r', '--results')
	parser.add_argument('-c', '--cores', type=int)
	parser.add_argument('-f', '--fold', type=int)
	args = parser.parse_args()

	if args.data:
		c.data_path = args.data
	if args.intermediate:
		c.intermediate_path = args.intermediate
	if args.results:
		c.results_path = args.results
	if args.cores:
		c.number_of_cores = args.cores

	if args.fold and 0 <= args.fold < c.number_of_folds:
		run_pconsc(args.fold)
	else:
		for k in range(c.number_of_folds):
			run_pconsc(k)
