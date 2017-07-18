#!/usr/bin/env python2
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


def chunks(l, n):
    '''Yield successive n-sized chunks from l'''
    # http://stackoverflow.com/questions/312443
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def write_seq(key, seq, linelen=80):
    '''wrangle a fasta seq from a key and sequence string'''
    seq = "".join([letter + '\n' for letter in chunks(seq, linelen)])
    fasta = ">%s\n%s" % (key, seq)
    return fasta


def evolve_ref(modification):
    # ie 'T/A' or 'T/A/C' need to sort
    modification = modification.split('/')
    non_diploid_flag = None
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
        return modifications.lower()
    else:
        return modifications


sample_dict = {}
with open('./final_results/final_table_python.varfix.csv') as f:
    csv_reader = csv.reader(f)
    csv_reader.next()  # dump the header
    for row in csv_reader:
        sample = row[0]
        call = evolve_ref(row[10])
        if sample in sample_dict:
            sample_dict[sample].append(call)
        else:
            sample_dict[sample] = [call]

with open('./final_results/all_sequence_files.fas', 'w') as f:
    for sample in sample_dict:
        seq = ''.join(sample_dict[sample])
        fasta = write_seq(sample, seq)
        f.write(fasta)

'''
for fil in sample_files:
    print fil
    result_dict = {}
    target_csv = "%s/%s" % (genotype_dir, fil)
    with open(target_csv) as f:
        data = [data for data in csv.reader(f)]
    seq_dict_mix = copy.deepcopy(seq_dict)
    scores = []
    for row in data:
        gene = row[1]
        pos = int(row[2]) - 1
        seq_dict_mix[gene][pos] = evolve_ref(row[13])
        scores.append(float(row[16]))
    # FJ9-S_S16 WARNING - this requres this format?
    percent_single = int(row[0])
    percent_mix = 100 - percent_single
    single_sample_name = fil.split('_&_')[0]
    # this doesnt work with unknow as their format is:12-0056
    #sample_name = single_sample_name.split('-')[0]
    # just use the first part
    sample_name = single_sample_name # tmp fix
    confidence_score = make_confidence_score(scores)
    single_sample_id = "%s:SC:%s:%.1f" % (sample_name, percent_single,
                                          confidence_score)

    mix_sample_id = "%s:IND:%s:%.1f" % (sample_name, percent_mix,
                                        confidence_score)
    # make the concatinated MLSTs single col
    singleseq = all_seq_calls[single_sample_name]
    singleseq = write_seq(single_sample_id, "".join(singleseq))
    seq_outfile.write(singleseq)
    # make the concatinated MLSTs mix col
    mixseq = [remove_primers(gene, "".join(seq_dict_mix[gene]))
              for gene in concat_order]
    mixseq = write_seq(mix_sample_id, "".join(mixseq))
    seq_outfile.write(mixseq)
seq_outfile.close()
'''
