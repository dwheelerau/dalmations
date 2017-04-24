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
    """Yield successive n-sized chunks from l."""
    # http://stackoverflow.com/questions/312443
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def write_seq(key, seq, linelen=80):
    '''wrangle a fasta seq from a key and sequence string'''
    seq = "".join([letter + '\n' for letter in chunks(seq, linelen)])
    fasta = ">%s\n%s" % (key, seq)
    return fasta


def make_confidence_score(scores):
    scores.sort()
    ave = sum(scores) / len(scores)
    max_ = scores[-1]
    result = ave * max_
    return result


def evolve_ref(modification):
    # ie 'T/A' or 'T/A/C' need to sort
    modification = modification.split('/')
    letters = []
    for letter in modification:
        # deal with AGG type geneotypes for triploids
        if len(letter) > 1:
            for l in letter:
                letters.append(l)
        else:
            letters.append(letter)

    letters = list(set(letters))
    letters.sort()
    letters = "".join(letters)
    modifications = IUPAC_dict[letters]
    return modifications


def remove_primers(gene, seq):
    cords = refcord_dict[gene]
    seq = seq[cords[0]: cords[1] - 1]
    return seq


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

# make the reference sequence just once
# TODO: this probably is not what I want
refseq = [remove_primers(gene, "".join(seq_dict[gene]))
          for gene in concat_order]
refseq = write_seq("refMLST", "".join(refseq))
seq_outfile = open('./final_sequences/sequenes.fa', 'w')
seq_outfile.write(refseq)


for fil in sample_files:
    print fil
    result_dict = {}
    target_csv = "%s/%s" % (genotype_dir, fil)
    with open(target_csv) as f:
        data = [data for data in csv.reader(f)]
    seq_dict_single = copy.deepcopy(seq_dict)
    seq_dict_mix = copy.deepcopy(seq_dict)
    scores = []
    for row in data:
        gene = row[1]
        pos = int(row[2]) - 1
        modifications = [evolve_ref(row[10]), evolve_ref(row[13])]
        seq_dict_single[gene][pos] = modifications[0]
        seq_dict_mix[gene][pos] = modifications[1]
        scores.append(float(row[16]))
    # FJ9-S_S16 WARNING - this requres this format?
    percent_single = int(row[0])
    percent_mix = 100 - percent_single
    sample_name = fil.split('_&_')[0].split('-')[0]
    confidence_score = make_confidence_score(scores)
    single_sample_name = "%s:SC:%s:%.1f" % (sample_name, percent_single,
                                            confidence_score)

    mix_sample_name = "%s:IND:%s:%.1f" % (sample_name, percent_mix,
                                          confidence_score)
    # make the concatinated MLSTs single col
    singleseq = [remove_primers(gene, "".join(seq_dict_single[gene]))
                 for gene in concat_order]
    singleseq = write_seq(single_sample_name, "".join(singleseq))
    seq_outfile.write(singleseq)
    # make the concatinated MLSTs mix col
    mixseq = [remove_primers(gene, "".join(seq_dict_mix[gene]))
              for gene in concat_order]
    mixseq = write_seq(mix_sample_name, "".join(mixseq))
    seq_outfile.write(mixseq)
seq_outfile.close()
