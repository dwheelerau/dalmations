#!/usr/bin/env python2

import os
import csv
##
# use genotpyes to extract sequence files
##
genotpye_dir = "./final_genotypes"
sample_files = next(os.walk(genotpye_dir))[2]

for fil in sample_files:
    best = 0
    flag = 0
    result_dict = {}
    with open(fil) as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if row[0] == 'percentage':
                flag == 1
            if flag == 1 and best == 0:
                best = int(row[0])
                gene = row[1]
                result_dict[gene] = bits
            else:
                pass
