#!/usr/bin/env python
import csv

# this is the index, each row repressents a different genotypic outcome
# I run each outcome against the freq of A going from 0 to 100.
# I create a dictionary that holds the allele 1 and allele 2 totols for
# each genotype (row) and each frequency (0-100). The index_key dict
# lets you calcualte the best genotype for a given frequency based
# on difference between O - E.
# TODO: 
# 1. hock this up to a GUI that allows strain selections
# 2. ATM only non-ref alleles in the mix are explored

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

data_dict = {}
with open('NZGL02259_final_table.csv') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        # NOTE: if non-ref
        # ONLY LOOK AT non-ref VARS
        # if row[-1].find("/") > 0:
        # {'strain':{gene:{pos:genotype}}}
        strain = row[0]
        gene = row[1]
        pos = row[2]
        genotype = row[-1]
        data_dict.setdefault(
            strain, {}).setdefault(gene, {})[pos] = (genotype, row[6:10])

# set percent wiggle to accept or reject a genotpye solution
WIGGLE = 5
SINGLE_STRAIN = "HUN91-S_S18"
MIX_STRAIN = "P1-90-10_S37"

# some variables for main script
nucleotides = ["A", "C", "G", "T"]
results = []

log = open('data_log.txt', 'w')
percent_log = {}

for percent in range(100):
    percent = 100 - percent
    log.write("Percent strain 1: %s\n" % percent)
    pass10 = 0

    # start looping through MLST one gene at a time
    remainder_counter = 0
    non_diploid_record = []
    diploid_counter = 0
    mlst_log = []
    for gene in data_dict[MIX_STRAIN]:
        gene_log = []
        log.write("gene: %s\n" % gene)

        # start loop through each gene
        non_rev_var = [ntpos for ntpos in data_dict[MIX_STRAIN][gene]
                       if data_dict[MIX_STRAIN][gene][ntpos][0].find('/') > 0]
        non_rev_var.sort(key=int)

        for pos in non_rev_var:  # data_dict[MIX_STRAIN][gene]
            log.write("position: %s\n" % pos)

            # set Single colony ID
            single_colony_call = data_dict[
                SINGLE_STRAIN][gene][pos][0].split('/')
            mixed_colony_data = [
                float(num) for num in data_dict[MIX_STRAIN][gene][pos][1]]
            mixed_colony_call = data_dict[MIX_STRAIN][gene][pos][0]

            log.write("single colony call: %s\n" % single_colony_call)
            log.write("Obs mixed data: %s\n" % mixed_colony_data)
            log.write("mixed data genotype: %s\n" % mixed_colony_call)

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
            log.write("allele 1: %s\n" % allele1)
            log.write("allele 2: %s\n" % allele2)

            allele1_obs = mixed_colony_data[nucleotides.index(allele1)]
            allele2_obs = mixed_colony_data[nucleotides.index(allele2)]
            log.write("allele 1 obs: %s\n" % allele1_obs)
            log.write("allele 2 obs: %s\n" % allele2_obs)

            possible_genotypes = []

            # test all genotypes to find best fit with Obs
            for row in index_key:
                # TMP: limit to diploids: row 8 is "8
                # ['1/1', '11/2', 'dip/tri']" see index_key[8]
                # if row < 8:
                if index_key[row][0] == '1/2' and diploid_ref == True:
                    possible_genotypes.append(row)
                else:
                    if index_key[row][0] == '1/1' and diploid_ref == False:
                        possible_genotypes.append(row)
            smallest_difference = (1000000.0, [])
            for row in possible_genotypes:
                allele1_exp, allele2_exp = freq_dict[percent][row]
                difference = abs(
                    allele1_obs - allele1_exp) + abs(allele2_obs - allele2_exp)
                if difference < smallest_difference[0]:
                    smallest_difference = (difference, row)

            # PASS: if smallest difference is WIGGLE%
            if smallest_difference[0] < WIGGLE:
                pass10 += 1
            if smallest_difference[1] > 7:
                non_diploid_record.append(smallest_difference[1])
            else:
                diploid_counter += 1

            # keep track of the number of differences for this percentage
            remainder_counter = remainder_counter + smallest_difference[0]

            log.write("smallest difference: %s %s\n" % (
                smallest_difference[0], index_key[smallest_difference[1]]))
            # log the data in a format that Jan recognises
            jan_data = [percent, SINGLE_STRAIN, MIX_STRAIN, gene, pos,
                        '/'.join(single_colony_call), mixed_colony_data[0],
                        mixed_colony_data[1], mixed_colony_data[2],
                        mixed_colony_data[3], mixed_colony_call,
                        smallest_difference[0],
                        ';'.join(index_key[smallest_difference[1]])]
            gene_log.append(jan_data)
            # jan_writer.writerow(jan_data)
        mlst_log.append(gene_log)

    # scan through non-diploids and record how many of each type
    found = []
    genotypes = [("normal", diploid_counter)]
    for idx in non_diploid_record:
        if idx not in found:
            count = non_diploid_record.count(idx)
            found.append(idx)
            genotype = index_key[idx][-1]
            genotypes.append((genotype, count))

    # this is the summary of the entire MLST for this percentage mix
    results.append((percent, pass10, remainder_counter))
    final_scores = (percent, pass10, remainder_counter, genotypes)
    log.write("Number that passed 10%% threshold: %s\n" % pass10)
    log.write("-----------------\n")
    percent_log[percent] = [final_scores, mlst_log]

# now process the results, sort by most wins, then by least remander
results = sorted(results, key=lambda x: (-x[1], x[2]))

# iterate through results and write out data (best will be at top of file)
jan_output = open('jan_output.csv', 'w')
jan_writer = csv.writer(jan_output)
header = ["percent", "single", "mix", "gene", "pos", "single_call",
          "A", "C", "G", "T", "mix_call", "remainder", "best",
          "pass_cut", "tot_unexplained", "genotypes"]
jan_writer.writerow(header)

for result in results:
    percent = result[0]
    percent_data = percent_log[percent]
    pass_cut = percent_data[0][1]
    remainder = percent_data[0][2]
    final_genotypes = percent_data[0][3]
    for mlst in percent_data[1]:
        for gene in mlst:
            gene += [pass_cut, remainder, final_genotypes]
            jan_writer.writerow(gene)
jan_output.close()

# close logfiles
log.close()
