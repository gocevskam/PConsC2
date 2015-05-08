import constants as c

import argparse
import sys

def run_pconsc(fold):
	print fold

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Run PConsC')
	parser.add_argument('-d', '--data')
	parser.add_argument('-i', '--intermediate')
	parser.add_argument('-r', '--results')
	parser.add_argument('-f', '--fold', type=int)
	args = parser.parse_args()

	if args.data:
		c.data_path = args.data
	if args.intermediate:
		c.intermediate_path = args.intermediate
	if args.results:
		c.results_path = args.results

	if args.fold and 0 <= args.fold < c.number_of_folds:
		run_pconsc(args.fold)
	else:
		for k in range(c.number_of_folds):
			run_pconsc(k)
