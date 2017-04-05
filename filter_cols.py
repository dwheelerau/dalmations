#!/usr/bin/env python

import sys
import csv

# Fitler param
left_size_limit = 250  # remove low quality seq
# primer lengths to chop off this sequencegene:  gene: (forward, reverese)
primer_dict = {'AAT1a': (21, 370),
               'ACC1': (20, 382),
               'ADP1': (22, 375),
               'MPI': (21, 377),
               'SYA1': (20, 363),
               'VPS13': (20, 395),
               'ZWF1b': (22, 385)}

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
            gene = bits[0]
            primer_f = primer_dict[gene][0]
            pos = int(bits[1])
            if pos <= left_size_limit and pos > primer_f:
                # len(14) is if the a/t etc non-ref col is added
                # turn this off and just output all data
                if len(bits) == 14:
                    output = bits[:5] + bits[9:]
                else:
                    # just add the reference call to the end
                    bits.append(bits[2])
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
            gene = bits[0]
            primer_r = primer_dict[gene][1]

            pos = int(bits[1])
            if pos > left_size_limit and pos < primer_r:
                # as above
                if len(bits) == 14:
                    output = bits[:5] + bits[9:]
                else:
                    bits.append(bits[2])
                    output = bits[:5] + bits[9:]
                output.insert(0, sample)
                outfile_csv.writerow(output)
                final_csv.writerow(output)

outfile.close()
final_outfile.close()
