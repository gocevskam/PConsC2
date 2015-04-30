data_path = 'data/'
intermediate_path = 'intermediate/'
results_path = 'results/'

alignments = [a + '_' + str(e) for a in ('hhblits', 'jackhmmer') for e in (1, -4, -10, -40)]
methods = ['psicov', 'plmdca']

combined_methods = [a + '_' + m for a in alignments for m in methods]

min_separation = 5

folds = 5
