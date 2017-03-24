#!/usr/bin/env python

# this is the index, each row repressents a different genotypic outcome
# I run each outcome against the freq of A going from 0 to 100.
# I create a dictionary that holds the allele 1 and allele 2 totols for
# each genotype (row) and each frequency (0-100). The index_key dict
# lets you calcualte the best genotype for a given frequency based
# on difference between O - E.
# Unused: from collections import defaultdict

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

# parse through single table and get geneotype for each
single_dict = {}

with open('single.csv') as f:
    for row in f:
        row = row.strip().split(",")
        # {'strain':{gene:{pos:genotype}}}
        strain = row[0]
        gene = row[1]
        pos = row[2]
        genotype = row[-1]
        single_dict.setdefault(strain,
                               {}).setdefault(gene, {})[pos] = genotype

# lets do the same with the other data but only collect varients
# (these are informative)
# mixed_dict['P1-9010_S81'][gene][pos] -> returns ('C/T',
# ['0', '52', '0', '48'])
mixed_dict = {}

with open('mixed.csv') as f:
    for row in f:
        row = row.strip().split(",")
        # NOTE: if non-ref
        if row[-1].find("/") > 0:
            # {'strain':{gene:{pos:genotype}}}
            strain = row[0]
            gene = row[1]
            pos = row[2]
            genotype = row[-1]
            mixed_dict.setdefault(
                strain, {}).setdefault(gene, {})[pos] = (genotype, row[6:10])

# some variables for main script
nucleotides = ["A", "C", "G", "T"]
results = []

# set percent wiggle to accept or reject a genotpye solution
WIGGLE = 5

log = open('data_log.txt', 'w')

for percent in range(100):
    percent = 100 - percent
    log.write("Percent strain 1: %s\n" % percent)
    pass10 = 0

    # start looping through MLST one gene at a time
    remainder_counter = 0
    non_diploid_count = 0
    for gene in mixed_dict['P1-9010_S81']:
        log.write("gene: %s\n" % gene)

        # start loop through each gene
        for pos in mixed_dict['P1-9010_S81'][gene]:
            log.write("position: %s\n" % pos)

            # set Single colony ID
            single_colony_call = single_dict[
                'hp11vw-S_S20'][gene][pos].split('/')
            mixed_colony_data = [
                float(num) for num in mixed_dict['P1-9010_S81'][gene][pos][1]]
            mixed_colony_call = mixed_dict['P1-9010_S81'][gene][pos][0]

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
                non_diploid_count += 1

            # keep track of the number of differences for this percentage
            remainder_counter = remainder_counter + smallest_difference[0]
            # non_diploid_count

            log.write("smallest difference: %s %s\n" % (
                smallest_difference[0], index_key[smallest_difference[1]]))
            # log.write("TTTT %s") % index_key[smallest_difference[1]]

    # this is the summary of the entire MLST for this percentage mix
    results.append((percent, pass10, remainder_counter, non_diploid_count))
    log.write("Number that passed 10%% threshold: %s\n" % pass10)
    log.write("-----------------\n")

# close logfile
log.close()
