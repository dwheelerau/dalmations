#!/usr/bin/env python
import subprocess
import os
import csv
#from Bio import SeqIO


def read_fastq(fname):
    '''read fastq files and grab sequnce, returns list of seq in file'''
    marker = 2
    counter = 1
    seqs = []
    with open(fname) as f:
        for line in f:
            if counter == marker:
                seqs.append(line)  # keep new line
                marker += 4
                counter += 1
            else:
                counter += 1
    return seqs


def rev_comp(seq_string):
    rc = []
    for letter in seq_string:
        if letter.upper() == "A":
            rc.insert(0, "T")
        elif letter.upper() == "C":
            rc.insert(0, "G")
        elif letter.upper() == "G":
            rc.insert(0, "C")
        else:
            if letter.upper() == "T":
                rc.insert(0, "A")
            else:
                # add new line to the end
                assert letter == "\n"
                rc.append(letter)
    assert len(rc) == len(seq_string)
    return "".join(rc)


def nuc_counter(col):
    A = col.count('A')
    C = col.count('C')
    G = col.count('G')
    T = col.count('T')
    depth = A + C + G + T
    return (A, C, G, T, depth)

# colect reference sequences in a dictionary
ref_dict = {}
gene = ""
with open('./reference_mlst/mlst.fa')as f:
    data = f.read().strip().split('\n')
    for line in data:
        if line[0] == ">":
            gene = line.strip()[1:]
        else:
            ref_dict[gene] = line.strip()

sample_dir = "samples_test"

target_files = [('AAT1apft.fastq', 'AAT1aprt.fastq'),
                ('ACC1pft.fastq', 'ACC1prt.fastq'),
                ('ADP1pft.fastq', 'ADP1prt.fastq'),
                ('MPIpft.fastq', 'MPIprt.fastq'),
                ('SYA1pft.fastq', 'SYA1prt.fastq'),
                ('VPS13pft.fastq', 'VPS13prt.fastq'),
                ('ZWF1bpft.fastq', 'ZWF1bprt.fastq')]

sample_dirs = next(os.walk(sample_dir))[1]

# main commands
#readcount = '/home/dwheeler/software_tools/bam-readcount-master/bin/bam-readcount --max-warnings 0 -f reference_mlst/mlst.fa %s %s | cut -f1,2,3,4,6-9 > %s'
#proctab = "python process_tables.py %s %s"
#filttab = "python filter_cols.py %s %s"

# add header, close, then filter_cols.py will append to this
outfile = open('final_results/test_table.csv', 'w')
csv_writer = csv.writer(outfile)
csv_writer.writerow(['Sample', 'loci', 'pos', 'ref',
                     'read', 'depth', 'A_freq', 'C_freq',
                     'G_freq', 'T_freq', 'non_ref'])
# write header once then close off, will append results from filter_col.py
outfile.close()

for sample in sample_dirs:
    for pair in target_files:
        outdir = "%s/%s/" % (sample_dir, sample)  # sample/DIR/
        # do text based alnment
        locus = pair[0].split('.fastq')[0][:-3]
        targetf = outdir + pair[0]
        seqf = read_fastq(targetf)
        targetr = outdir + pair[1]
        seqr = read_fastq(targetr)
        seqrc = [rev_comp(read) for read in seqr]
        alnf = targetf.replace("fastq", "aln")
        with open(alnf, "w") as f:
            for seq in seqf:
                f.write(seq)
        alnr = targetr.replace("fastq", "aln")
        with open(alnr, "w") as f:
            for seq in seqr:
                f.write(seq)
        # BROCKEN: can't use zip
        with open(alnf) as f:
            data = f.read().strip().split('\n')
            alnf_cols = zip(*data)
        with open(alnr) as f:
            data = f.read().strip().split('\n')
            alnr_cols = zip(*data)

        alnf_data = alnf.replace("aln", "aln_data")
        with open(alnf_data, "w") as f:
            pos_counter = 0
            for col in alnf_cols:
                data = nuc_counter(col)
                ref = ref_dict[locus][pos_counter]
                line = "%s\t%s\t%s\t%s\tA:%s\tC:%s\tG:%s\tT:%s\n" % (
                    locus, pos_counter + 1, ref, data[-1], data[0], data[1],
                    data[2], data[3])
                pos_counter += 1
                f.write(line)
        # BROCKEN: how to deal with reference calls in reverse?
        alnr_data = alnr.replace("aln", "aln_data")
        with open(alnr_data, "w") as f:
            pos_counter = 1
            for col in alnr_cols:
                data = nuc_counter(col)
                line = "%s\t%s\t%s\t%s\tA:%s\tC:%s\tG:%s\tT:%s\n" % (
                    locus, pos_counter, "N", data[-1], data[0], data[1],
                    data[2], data[3])
                pos_counter += 1
                f.write(line)

print "done"
"""
        # readcount command infile, locus, outfile
        print pair[0][:-9]
        readcountcmd1 = readcount % (targetf.split(".")[0]+".sorted.bam",
                                     pair[0][:-9],
                                     targetf.split(".")[0]+".counts")
        res = subprocess.check_output(readcountcmd1, shell=True)
        readcountcmd2 = readcount % (targetr.split(".")[0]+".sorted.bam",
                                     pair[0][:-9],
                                     targetr.split(".")[0]+".counts")
        res = subprocess.check_output(readcountcmd2, shell=True)

        # run process_table.py on frw and rev reads, py handles output
        proctabcmd = proctab % (targetf.split(".")[0]+".counts",
                                targetr.split(".")[0]+".counts")
        res = subprocess.check_output(proctabcmd, shell=True)

        # filter cols using python script, py handles output
        filttabcmd = filttab % (targetf.split(".")[0]+".counts.table",
                                targetr.split(".")[0]+".counts.table")
        res = subprocess.check_output(filttabcmd, shell=True)

print "done"
"""
