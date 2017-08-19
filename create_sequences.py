#!/usr/bin/env python2

import copy
import os
import csv
##
# use genotpyes to extract sequence files
##
# this is to remove primer sequences
# cords = refcord_dict['AAT1a']
# seq[cords[0]: cords[1]-1] # note minus one
# data dictionaries
IUPAC_dict = {'A': 'A',
              'C': 'C',
              'G': 'G',
              'T': 'T',
              'AG': 'R',
              'CT': 'Y',
              'CG': 'S',
              'AT': 'W',
              'GT': 'K',
              'AC': 'M',
              'CGT': 'B',
              'AGT': 'D',
              'ACT': 'H',
              'ACG': 'V',
              'ACGT': 'N'}


refcord_dict = {'AAT1a': (21, 370),
                'ACC1': (20, 382),
                'ADP1': (22, 375),
                'MPI': (21, 377),
                'SYA1': (20, 363),
                'VPS13': (20, 395),
                'ZWF1b': (22, 385)}


def chunks(l, n):
    '''Yield successive n-sized chunks from l'''
    # http://stackoverflow.com/questions/312443
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def write_seq(key, seq, linelen=80, desc=''):
    '''wrangle a fasta seq from a key and sequence string'''
    seq = "".join([letter + '\n' for letter in chunks(seq, linelen)])
    fasta = ">%s %s\n%s" % (key, desc, seq)
    return fasta


def make_confidence_score(scores):
    scores.sort()
    ave = sum(scores) / len(scores)
    max_ = scores[-1]
    result = ave * max_
    return result


def evolve_ref(modification):
    # ie 'T/A' or 'T/A/C' need to sort
    non_diploid_flag = None
    modification = modification.split('/')
    letters = []
    for letter in modification:
        # deal with AGG type geneotypes for triploids
        if len(letter) > 1:
            for l in letter:
                letters.append(l)
        else:
            letters.append(letter)

    if len(letters) > 2:
        non_diploid_flag = 1
    letters = list(set(letters))
    letters.sort()
    letters = "".join(letters)
    modifications = IUPAC_dict[letters]
    if non_diploid_flag == 1:
        # lowercase geneotypes that are not diploid
        return modifications.lower()
    else:
        return modifications


def remove_primers(gene, seq):
    cords = refcord_dict[gene]
    seq = seq[cords[0]: cords[1] - 1]
    return seq


def check_genotype(calls):
    '''checks calls,tests 50/50 or 100/0, returns 0 if yes and 1 if no'''
    calls_int = [int(c) for c in calls]
    calls_int.sort(reverse=True)
    # this should be >85 if 100/0
    if calls_int[0] >= 95:
        return 0
    # this should be >45 if 55/45 or 50/50 ie second value is smallest
    elif calls_int[1] >= 45:
        return 0
    else:
        return 1

# make sure we are in the base directory in case run from GUI
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

seq_dict = {}
with open('./reference_mlst/mlst.fa') as f:
    for line in f:
        if line[0] == '>':
            key = line.strip()[1:]
            continue
        elif len(line) > 1:
            seq_dict[key] = list(line.strip())

# it might be better to run this on single files through
# sys.argv and just loop through file list instead
genotype_dir = "./final_genotypes"
sample_files = []
for f in os.listdir(genotype_dir):
    if f.endswith(".csv"):
        sample_files.append(f)

concat_order = seq_dict.keys()
# by alphabet
concat_order.sort()

# make a dict of all mlst posns for single sample calls which
# are not in the summary tables (these only contain non-ref mix
# calls). Modify the var nts using the same fn. These contain no primers.
single_seq_calls = {}
# this is only used for the single col calls, so I'm going to lowercase
# anything here that has a strange genotpye (ie ! 100/0 or 50/50), this will
# obviosuly effect mix genotypes but that is OK because those are ignored
# changed this to be dict of samples and genes
with open('./final_results/final_table_python.csv') as f:
    csv_reader = csv.reader(f)
    csv_reader.next()  # dump the header
    for row in csv_reader:
        sample = row[0]
        gene = row[1]
        pos = row[2]
        call = evolve_ref(row[-2])  # if non-ref will be in this col
        obs_calls = row[6:10]
        # I only want this for single col calls
        if check_genotype(obs_calls) == 1:
            call = call.lower()
        # lowercase because calls are not 100/0 or 50/50
        # only effects single col calls as this dict is only used for those

        if sample in single_seq_calls:
            if gene in single_seq_calls[sample]:
                single_seq_calls[sample][gene][pos] = call
            else:
                single_seq_calls[sample][gene] = {pos: call}
        else:
            single_seq_calls[sample] = {gene: {pos: call}}

# not effecient
mix_seq_calls = {}
with open('./final_results/final_table_python.csv') as f:
    csv_reader = csv.reader(f)
    csv_reader.next()  # dump the header
    for row in csv_reader:
        sample = row[0]
        gene = row[1]
        pos = row[2]
        call = evolve_ref(row[-2])  # if non-ref will be in this col
        obs_calls = row[6:10]
        if sample in mix_seq_calls:
            if gene in mix_seq_calls[sample]:
                mix_seq_calls[sample][gene][pos] = call
            else:
                mix_seq_calls[sample][gene] = {pos: call}
        else:
            mix_seq_calls[sample] = {gene: {pos: call}}


# make a copy of this to 
# make the reference sequence just once
# TODO: this probably is not what I want
refseq = [remove_primers(gene, "".join(seq_dict[gene]))
          for gene in concat_order]
refseq = write_seq("refMLST", "".join(refseq))
seq_outfile = open('./final_sequences/sequences.fa', 'w')
seq_outfile.write(refseq)

# a place to store sequences that have already been made
single_seq_used = []

for fil in sample_files:
    result_dict = {}
    target_csv = "%s/%s" % (genotype_dir, fil)
    single_sample_name = fil.split('_&_')[0]
    mix_sample_name = fil.split('_&_')[1].split('.csv')[0]
    # do the single sequence first, then use the derived genotpyes to morp
    # this into a new dervied seq for mix col
    # the derived nt calls are in these files
    with open(target_csv) as f:
        data = [data for data in csv.reader(f)]
    # seq_dict_mix = copy.deepcopy(seq_dict)
    scores = []
    # this modifies single seq seq to contain mix calls
    for row in data:
        gene = row[1]
        # pos = (row[2]) - 1
        pos = row[2]
        # seq_dict_mix[gene][pos] = evolve_ref(row[13])
        mix_seq_calls[mix_sample_name][gene][pos] = evolve_ref(row[13])
        scores.append(float(row[16]))
    percent_single = int(row[0])
    percent_mix = 100 - percent_single
    # this doesnt work with unknow as their format is:12-0056
    # sample_name = single_sample_name.split('-')[0]
    # just use the first part
    sample_name = single_sample_name  # tmp fix
    # confidence_score = make_confidence_score(scores)
    # single_sample_id = "%s:SC:%s:%.1f" % (sample_name, percent_single)  #,
    #                                      # confidence_score)
    mix_sample_id = "%s:IND:%s" % (sample_name, percent_mix)
    # single_sample_id = "%s:SC:%s:%.1f" % (sample_name, percent_single)  #,
                                        # confidence_score)
    single_sample_id = "%s:SC:%s" % (sample_name, percent_single)
    # make the concatinated MLSTs single col
    if sample_name not in single_seq_used:
        # singleseq = all_seq_calls[single_sample_name]
        singleseq = []
        for gene in concat_order:
            # need to sort the positions, NOTE keys are strings!!!!
            ordered_pos = [int(p)
                           for p in single_seq_calls[single_sample_name][gene].keys()]
            ordered_pos.sort()
            for pos in ordered_pos:
                for nt in single_seq_calls[single_sample_name][gene][str(pos)]:
                    singleseq.append(nt)
        singleseq = write_seq(single_sample_id, "".join(singleseq))
        seq_outfile.write(singleseq)
        single_seq_used.append(sample_name)
    # make the concatinated MLSTs mix col
    # now we remake the sequence again with the updated calls
    mixseq = []
    for gene in concat_order:
        # need to sort the positions, NOTE keys are strings!!!!
        ordered_pos = [int(p)
                       for p in mix_seq_calls[mix_sample_name][gene].keys()]
        ordered_pos.sort()
        for pos in ordered_pos:
            for nt in mix_seq_calls[mix_sample_name][gene][str(pos)]:
                mixseq.append(nt)


       # mixseq = [remove_primers(gene, "".join(seq_dict_mix[gene]))
    #           for gene in concat_order]
    mixseq = write_seq(mix_sample_id, "".join(mixseq), desc=fil)
    seq_outfile.write(mixseq)
seq_outfile.close()
