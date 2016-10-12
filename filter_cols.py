#!/usr/bin/env python

import sys
import csv
# Fitler param
pos_limit = 230  # remove low quality seq

left = sys.argv[1]
sample = left.split('/')[-2]
outfile = open(left+"final.csv", "w")
outfile_csv = csv.writer(outfile)
# append, orig created by run script which also add the header
final_outfile = open('final_results/final_table.csv', 'a')
final_csv = csv.writer(final_outfile)

with open(left) as f:
    for line in f:
        bits = line.strip().split("\t")
        if line[0] == "l":
            header = bits[:5] + bits[9:]
            header.insert(0, "Sample")
            outfile_csv.writerow(header)
        else:
            pos = int(bits[1])
            if pos <= pos_limit:
                if len(bits) == 14:
                    output = bits[:5] + bits[9:]
                    # first gene, only want sample recorded once
                    output.insert(0, sample)
                    outfile_csv.writerow(output)
                    final_csv.writerow(output)
right = sys.argv[2]
with open(right) as f:
    for line in f:
        bits = line.strip().split("\t")
        if line[0] == "l":
            pass
        else:
            pos = int(bits[1])
            if pos > pos_limit:
                if len(bits) == 14:
                    output = bits[:5] + bits[9:]
                    output.insert(0, sample)
                    outfile_csv.writerow(output)
                    final_csv.writerow(output)

outfile.close()
final_outfile.close()
