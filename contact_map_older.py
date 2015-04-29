import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plot

import sys

def read_sequence(file_name):
	with open(file_name, 'r') as f:
		f.readline()
		return f.readline().strip()

def read_contacts_matrix(file_name, n):
	contacts = np.zeros((n, n))
	with open(file_name, 'r') as f:
		for line in f:
			line = line.strip()
			if line:
				splitted = line.split()
				i = int(splitted[0])
				j = int(splitted[1])
				c = float(splitted[2])
				contacts[i-1, j-1] = c
				contacts[j-1, i-1] = c
	return contacts


if __name__ == "__main__":
	if len(sys.argv) < 2:
		print "Not enough arguments. Enter the path to the protein data."
	else:
		path = sys.argv[1]
		
		sequence = read_sequence(path + '/sequence.fa')
		n = len(sequence)
		contacts = read_contacts_matrix(path + '/contacts.CB', n)
		
		plot.matshow(contacts, origin='lower')
		plot.matshow(np.logical_or(contacts == 0, contacts >= 8), origin='lower', cmap=cm.gray)
		plot.show()

