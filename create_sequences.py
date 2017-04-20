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
    with open("./final_genotypes/FJ9-S_S16_&_P1-80-20_S36.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            if len(row) == 0:
                continue
            if row[0] == 'percent':
                print "flag %s best %s" % (best, flag)
                flag = 1
                continue
            if flag == 1 and best == 0:
                print "flag %s best %s" % (best, flag)
                best = int(row[0])
                gene = row[1]
                result_dict[gene] = [row]
                continue
            if int(row[0]) == best:
                if gene in result_dict:
                    result_dict[gene].append(row)
                else:
                    result_dict[gene] = [row]
            else:
                pass
