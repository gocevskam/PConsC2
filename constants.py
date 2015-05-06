data_path = 'data/'
intermediate_path = 'intermediate/'
results_path = 'results/'

number_of_cores = -1

alignments = [a + '_' + str(e) for a in ('hhblits', 'jackhmmer') for e in (1, -4, -10, -40)]
methods = ['psicov', 'plmdca']
combined_methods = [a + '_' + m for a in alignments for m in methods]

number_of_folds = 5

min_separation = 5
receptive_field = 3
