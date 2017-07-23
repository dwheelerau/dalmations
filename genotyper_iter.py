#!/usr/bin/env python
import csv
import sys
import os

# this is the index, each row repressents a different genotypic outcome
# I run each outcome against the freq of A going from 0 to 100.
# I create a dictionary that holds the allele 1 and allele 2 totols for
# each genotype (row) and each frequency (0-100). The index_key dict
# lets you calcualte the best genotype for a given frequency based
# on difference between O - E.
# 1. hock this up to a GUI that allows strain selections
# 2. ATM only non-ref alleles in the mix are explored

# make sure we are in the base directory in case run from GUI
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

try:
    assert len(sys.argv) == 3
except AssertionError:
    print "usage: python2 genotyper_iter.py <SINGLE_COL_NAME> <MIX_COL_NAME>"
    exit(1)

print 'processing - tmp : %s %s' % (sys.argv[1], sys.argv[2])
index_key = {}
counter = 0
# contains genotype frequencies in binary format
with open('index_key.txt') as f:
    for line in f:
        index_key[counter] = line.strip().split('\t')
        counter += 1

# this data is the actual frequencies
A1 = [1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 0, 0,
      1.0, 1.0, 0.5, 0.5,
      1.0, 1.0, 0.5, 0.5,
      0.6666, 0.6666, 0.3333, 0.3333,
      0.6666, 0.6666, 0.3333, 0.3333,
      0.6666, 0.6666, 0.3333, 0.3333,
      0.75, 0.75, 0.25, 0.25,
      0.75, 0.75, 0.25, 0.25,
      0.75, 0.75, 0.25, 0.25]

A2 = [0, 0, 0, 0.5, 0.5, 0.5, 1.0, 1.0,
      0, 0, 0.5, 0.5,
      0, 0, 0.5, 0.5,
      0.3333, 0.3333, 0.6666, 0.6666,
      0.3333, 0.3333, 0.6666, 0.6666,
      0.3333, 0.3333, 0.6666, 0.6666,
      0.25, 0.25, 0.75, 0.75,
      0.25, 0.25, 0.75, 0.75,
      0.25, 0.25, 0.75, 0.75]

B1 = [1.0, 0.5, 0, 1.0, 0.5, 0, 1.0, 0.5,
      0.6666, 0.3333, 0.6666, 0.3333,
      0.75, 0.25, 0.75, 0.25,
      1.0, 0.5, 1.0, 0.25,
      0.6666, 0.3333, 0.6666, 0.3333,
      0.75, 0.25, 0.75, 0.25,
      1.0, 0.5, 1.0, 0.5,
      0.6666, 0.3333, 0.6666, 0.3333,
      0.75, 0.25, 0.75, 0.25]

B2 = [0, 0.5, 1.0, 0, 0.5, 1.0, 0, 0.5,
      0.3333, 0.6666, 0.3333, 0.6666,
      0.25, 0.75, 0.25, 0.75,
      0, 0.5, 0, 0.5,
      0.3333, 0.6666, 0.3333, 0.6666,
      0.25, 0.75, 0.25, 0.75,
      0, 0.5, 0, 0.5,
      0.3333, 0.6666, 0.3333, 0.6666,
      0.25, 0.75, 0.25, 0.75]

# go from 1 - 100 for freq of A, B is fixed so ignore
# the A values need to be passed the A freq and the B cols the b freq
freq_dict = {}

for freq in range(0, 101):
    freqA = freq
    freqB = 100 - freqA

    index_dict = {}

    for index in range(len(A1)):
        allele1_sum = (A1[index] * freqA) + (B1[index] * freqB)
        allele2_sum = (A2[index] * freqA) + (B2[index] * freqB)
        index_dict[index] = (allele1_sum, allele2_sum)
    freq_dict[freq] = index_dict

##########
# now you can get the allala1 sum and allele2 sums for
# strain A freq = 40 and row 0 by doing this
# freq_dict[40][0]
# returns: (100.0, 0)
# example2 freq 50 row 2
# freq_dict[50][2]
# (50.0, 50.0)

# lets do the same with the other data but only collect varients
# (these are informative)
# data_dict['MIX_STRAIN'][gene][pos] -> returns ('C/T',
# ['0', '52', '0', '48'])
##########

# set percent wiggle to accept or reject a genotpye solution
WIGGLE = 5

SINGLE_STRAIN = sys.argv[1]
# SINGLE_STRAIN = "FJ9-S_S16"
MIX_STRAIN = sys.argv[2]
# MIX_STRAIN = "P1-50-50_S35"
print SINGLE_STRAIN
print MIX_STRAIN
data_dict = {}
# this is the orginal file and default produce by aln scrip but
# it had some errors 
datafile = './final_results/final_table_python.csv'
with open(datafile) as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        # NOTE: if non-ref
        # ONLY LOOK AT non-ref VARS
        # if row[-1].find("/") > 0:
        # {'strain':{gene:{pos:genotype}}}
        strain = row[0]
        gene = row[1]
        pos = row[2]
        # genotype = row[-1] added sample to end so now this is genotype
        genotype = row[-2]
        data_dict.setdefault(
            strain, {}).setdefault(gene, {})[pos] = (genotype, row[6:10])


def genotyper(single_call, mix_call, geneotypes):
    strain2 = geneotypes.split(";")[1]
    try:
        assert len(mix_call) == 3
    except AssertionError:
        print mix_call
    if single_call.find("/") > 0:
        call1, call2 = single_call.split("/")
    else:
        call1 = single_call
        for letter in mix_call.split("/"):
            if letter != call1:
                call2 = letter
    strain2 = strain2.replace('1', call1)
    strain2 = strain2.replace('2', call2)
    return strain2


def calculate_diff(possible_genotypes, allele1_obs, allele2_obs, per):
    """O-E get get the smallest difference"""
    smallest_difference = (1000000.0, [])
    for row in possible_genotypes:
        allele1_exp, allele2_exp = freq_dict[per][row]
        difference = abs(
            allele1_obs - allele1_exp) + abs(allele2_obs - allele2_exp)
        if difference < smallest_difference[0]:
            smallest_difference = (difference, row)
    return smallest_difference


# some variables for main script
nucleotides = ["A", "C", "G", "T"]
results = []

percent_log = {}

for percent in range(100):
    percent = 100 - percent
    pass5 = 0

    # start looping through MLST one gene at a time
    remainder_counter = 0
    non_diploid_record = []
    diploid_counter = 0
    usefull_allele_counter = 0
    mlst_log = []
    try:
        genes = sorted(data_dict[MIX_STRAIN].keys())
    except KeyError:
        print "can't find %s in %s" % (MIX_STRAIN, datafile)
        exit(1)
    for gene in genes:
        gene_log = []

        # start loop through each gene
        non_ref_var = [ntpos for ntpos in data_dict[MIX_STRAIN][gene]
                       if data_dict[MIX_STRAIN][gene][ntpos][0].find('/') > 0]
        non_ref_var.sort(key=int)

        for pos in non_ref_var:  # data_dict[MIX_STRAIN][gene]
            usefull_allele_counter += 1
            # set Single colony ID
            try:
                single_colony_call = data_dict[
                    SINGLE_STRAIN][gene][pos][0].split('/')
            except KeyError:
                print "can't find %s in %s" % (SINGLE_STRAIN, datafile)
                exit(1)
            mixed_colony_data = [
                float(num) for num in data_dict[MIX_STRAIN][gene][pos][1]]
            mixed_colony_call = data_dict[MIX_STRAIN][gene][pos][0]

            if len(single_colony_call) == 2:
                allele1, allele2 = single_colony_call
                diploid_ref = True
            else:
                assert len(single_colony_call) == 1
                allele1 = single_colony_call[0]
                # find the other allele from the mixed genotype
                for nuc in mixed_colony_call.split('/'):
                    if nuc != allele1:
                        allele2 = nuc
                diploid_ref = False

            # throw exception: I don't think this should ever fail
            assert allele2

            allele1_obs = mixed_colony_data[nucleotides.index(allele1)]
            allele2_obs = mixed_colony_data[nucleotides.index(allele2)]
            possible_genotypes = []
            alt_genotypes = []
            # test all genotypes to find best fit with Obs
            for row in index_key:
                # TMP: limit to diploids: row 8 is "8
                # ['1/1', '11/2', 'dip/tri']" see index_key[8]
                if row < 8:
                    if index_key[row][0] == '1/2' and diploid_ref == True:
                        possible_genotypes.append(row)
                    else:
                        if index_key[row][0] == '1/1' and diploid_ref == False:
                            possible_genotypes.append(row)
                else:
                    # these are triploid and other unlikely genotpyes
                    assert row >= 8
                    if index_key[row][0] == '1/2' and diploid_ref == True:
                        alt_genotypes.append(row)
                    else:
                        if index_key[row][0] == '1/1' and diploid_ref == False:
                            alt_genotypes.append(row)

            smallest_difference = calculate_diff(possible_genotypes,
                                                 allele1_obs, allele2_obs,
                                                 percent)

            # PASS: if smallest difference is WIGGLE%
            if smallest_difference[0] <= WIGGLE:
                pass5 += 1
            else:
                # try some rarer genotypes to see if can get better result
                any_better = calculate_diff(alt_genotypes,
                                            allele1_obs, allele2_obs,
                                            percent)
                if any_better[0] < smallest_difference[0]:
                    smallest_difference = any_better
            if smallest_difference[1] > 7:
                non_diploid_record.append(smallest_difference[1])
            else:
                diploid_counter += 1

            # keep track of the number of differences for this percentage
            remainder_counter = remainder_counter + smallest_difference[0]

            # grab the string genotypes for strain1 and strain2
            genotypes = ';'.join(index_key[smallest_difference[1]])
            # log the data in a format that Jan recognises
            single_colony_call = '/'.join(single_colony_call)
            strain2_genotype = genotyper(single_colony_call, mixed_colony_call,
                                         genotypes)
            jan_data = [percent, gene, pos, " ",
                        mixed_colony_data[0],
                        mixed_colony_data[1], mixed_colony_data[2],
                        mixed_colony_data[3], mixed_colony_call,
                        " ", single_colony_call, percent,
                        smallest_difference[0],
                        strain2_genotype]
            gene_log.append(jan_data)

        mlst_log.append(gene_log)

    # scan through non-diploids and record how many of each type
    found = []
    genotype_counts = [("normal", diploid_counter)]
    for idx in non_diploid_record:
        if idx not in found:
            count = non_diploid_record.count(idx)
            found.append(idx)
            genotype = index_key[idx][-1]
            genotype_counts.append((genotype, count))

    # this is the summary of the entire MLST for this percentage mix
    results.append((percent, pass5, remainder_counter))
    final_scores = (percent, pass5, remainder_counter, genotype_counts)
    percent_log[percent] = [final_scores, mlst_log]

# now process the results, sort by most wins, then by least remander
results = sorted(results, key=lambda x: (-x[1], x[2]))

# iterate through results and write out data (best will be at top of file)
# add check to make sure file DOESNOT Exists.
# jan_output = open(sys.argv[3]', 'w')
output_name = "./genotype_data/%s_&_%s.csv" % (SINGLE_STRAIN, MIX_STRAIN)
jan_output = open(output_name, 'w')

# formatting header information
jan_writer = csv.writer(jan_output)
jan_writer.writerow(["mix:", MIX_STRAIN, " ", usefull_allele_counter, "loci"])
jan_writer.writerow(["single:", SINGLE_STRAIN])
jan_writer.writerow([])
jan_writer.writerow([])
# insert subheading
sub_header = [" "] * 18
sub_header.insert(1, "loci")
sub_header.insert(4, "sequencing")
sub_header.insert(10, "strain1(SC)")
sub_header.insert(13, "strain2(INF)")
sub_header.insert(18, "inference scores across all loci")
jan_writer.writerow(sub_header)

header = ["percent", "gene", "pos", " ",
          "A", "C", "G", "T", "mix_call", " ", "single_call",
          "%", " ", "INF_call", "%", " ", "unexplained", " ",
          "pass_cut", "tot_unexplained", " ", "genotype"]
jan_writer.writerow(header)

# file to write out best result for reading by other scripts
script_output = "./final_genotypes/%s_&_%s.csv" % (SINGLE_STRAIN, MIX_STRAIN)
script_output_h = open(script_output, 'w')
script_writer = csv.writer(script_output_h)

flag = 0
best = 0

for result in results:
    percent = result[0]
    if flag == 0:
        # capture best result and write this to script_writer
        best = result[0]
        flag = 1
    percent_data = percent_log[percent]
    pass_cut = percent_data[0][1]
    remainder = percent_data[0][2]
    final_genotypes = percent_data[0][3]
    for mlst in percent_data[1]:
        for gene in mlst:
            gene += [100-percent, " ", gene.pop(12), " ",
                     "%s/%s" % (pass_cut, usefull_allele_counter),
                     remainder, " ", final_genotypes]
            gene.insert(12, " ")
            jan_writer.writerow(gene)
            if percent == best:
                script_writer.writerow(gene)
jan_output.close()
script_output_h.close()
