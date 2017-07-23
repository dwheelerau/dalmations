#!/usr/bin/env python
import os
import csv
import sys


def read_fastq(fname):
    '''read fastq files and grab seq, returns list of seq in file'''
    marker = 2
    counter = 1
    seqs = []
    with open(fname) as f:
        for line in f:
            if counter == marker:
                seqs.append(line)  # keep trailing new line '\n'
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
                try:
                    assert letter == "\n"
                except AssertionError:
                    print "Warning, non-normal nucleotide found: %s" % letter
                rc.append(letter)
    assert len(rc) == len(seq_string)
    return "".join(rc)


def nuc_counter(col):
    A = col.count('A')
    C = col.count('C')
    G = col.count('G')
    T = col.count('T')
    depth = A + C + G + T
    return [depth, A, C, G, T]


def cal_percents(count_list):
    """A,C,G,T, depth"""
    depth = float(count_list[0])
    if depth > 0:
        count_list.append(str(100*(int(count_list[1])/depth)))  # perA
        count_list.append(str(100*(int(count_list[2])/depth)))  # perC
        count_list.append(str(100*(int(count_list[3])/depth)))  # perG
        count_list.append(str(100*(int(count_list[4])/depth)))  # perT
    else:
        # div by zero error
        count_list.append('0.0')
        count_list.append('0.0')
        count_list.append('0.0')
        count_list.append('0.0')
    return count_list


def filter_data(data):
    """filter out noise and if greater than noise collect nt call"""
    # ACGT
    noise = 6.0
    choice = ["A", "C", "G", "T"]
    counter = 0
    # if 100% non-ref call will still show ref/alt
    result = []
    for per in data[7:]:
        # allows for floating pt ie 5.2 will be ignored
        if float(per) >= noise:
            call = choice[counter]
            if call not in result:
                result.append(call)
        else:
            pass
        # modify float in case it will be returned
        data[7+counter] = "%.0f" % (float(per))
        counter += 1
    if len(result) > 1:
        result = "/".join(result)
        data.append(result)
    elif len(result) == 1:
        result = "".join(result)
        data.append(result)
    return data

# need to change to the current directory in case of running GUI
# https://stackoverflow.com/questions/1432924/python-change-the-
# scripts-working-directory-to-the-scripts-own-directory

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# colect reference sequences in a dictionary
ref_dict = {}
gene = ""
with open('./reference_mlst/mlst.fa') as f:
    data = f.read().strip().split('\n')
    for line in data:
        if line[0] == ">":
            gene = line.strip()[1:]
        else:
            ref_dict[gene] = line.strip()


target_files = [('AAT1apft.fastq', 'AAT1aprt.fastq'),
                ('ACC1pft.fastq', 'ACC1prt.fastq'),
                ('ADP1pft.fastq', 'ADP1prt.fastq'),
                ('MPIpft.fastq', 'MPIprt.fastq'),
                ('SYA1pft.fastq', 'SYA1prt.fastq'),
                ('VPS13pft.fastq', 'VPS13prt.fastq'),
                ('ZWF1bpft.fastq', 'ZWF1bprt.fastq')]

# sample_dir = "samples_test"
try:
    sample_dir = sys.argv[1]
except IndexError:
    print 'Missing samples directory that contains the sequence files for'
    print ' your samples?'
    print 'usage: python2 run_aligner.py <sample_dir>'
    sys.exit(1)

try:
    sample_dirs = next(os.walk(sample_dir))[1]
except StopIteration:
    print 'Is the samples directory %s empty?' % sample_dir
    print 'usage: python2 run2.py <sample_dir>'
    sys.exit(1)

# add header overwrite and write header
outfile = open('final_results/final_table_python.csv', 'w')
csv_writer = csv.writer(outfile)
csv_writer.writerow(['Sample', 'loci', 'pos', 'ref',
                     'read', 'depth', 'A_freq', 'C_freq',
                     'G_freq', 'T_freq', 'call', 'sample_dir'])

# dict contains cords two splice so len(ft->+<-RT) == len(reference)
aln_slicer_dict = {'AAT1a': (224, 166),
                   'ACC1': (225, 176),
                   'ADP1': (225, 171),
                   'MPI': (225, 171),
                   'SYA1': (224, 159),
                   'VPS13': (225, 190),
                   'ZWF1b': (225, 179)}

# use this dict to remove alnments that don't include all of re
# this will prevent frameshift snps
reflen_dict = {'AAT1a': 390,
               'ACC1': 401,
               'ADP1': 396,
               'MPI': 396,
               'SYA1': 383,
               'VPS13': 415,
               'ZWF1b': 404}

primer_dict = {'AAT1a': (21, 370),
               'ACC1': (20, 382),
               'ADP1': (22, 375),
               'MPI': (21, 377),
               'SYA1': (20, 363),
               'VPS13': (20, 395),
               'ZWF1b': (22, 385)}


for sample in sample_dirs:
    print "Processing %s" % sample
    for pair in target_files:
        outdir = "%s/%s/" % (sample_dir, sample)  # sample/DIR/
        # do text based alnment
        locus = pair[0].split('.fastq')[0][:-3]
        targetf = outdir + pair[0]
        # get gene name so can slice seqs for proper aln
        fseq_length, rseq_length = aln_slicer_dict[locus]
        seqf = [sf[:fseq_length] + "\n" for sf in read_fastq(targetf)]
        targetr = outdir + pair[1]
        seqr = [r[:rseq_length] + "\n" for r in read_fastq(targetr)]
        seqrc = [rev_comp(read) for read in seqr]
        alnf = targetf.replace("fastq", "aln")
        with open(alnf, "w") as f:
            for seq in seqf:
                f.write(seq)
        # I need to slice the alignment before doing the RC
        # otherwise they are all different lenghts
        alnr = targetr.replace("fastq", "aln")
        with open(alnr, "w") as f:
            for seq in seqrc:
                f.write(seq)

        # zip should pair up the sequences again in tuples, watch newline
        aln_seqs = [part[0][:-1] + part[1]
                    for part in zip(seqf, seqrc)
                    if len(part[0][:-1] + part[1][:-1]) == reflen_dict[locus]]
        aln_data = alnf.replace("pft.aln", ".aln_data")
        with open(aln_data, 'w') as f:
            for seq in aln_seqs:
                f.write(seq)
        # transpose cols into lists ['aaaaa','tttttt','ggggggg']
        aln_cols = map(list, zip(*aln_seqs))[:-1]
        aln_info = alnf.replace("pft.aln", ".aln_info.csv")
        with open(aln_info, "w") as f:
            aln_info_writer = csv.writer(f)
            pos_counter = 1
            primers = primer_dict[locus]
            ref_seq = ref_dict[locus]
            for col in aln_cols:
                if pos_counter > primers[0] and pos_counter < primers[1]:
                    data = nuc_counter(col)
                    per_data = cal_percents(data)
                    ref = ref_seq[pos_counter-1]
                    per_data.insert(0, ref)
                    per_data.insert(0, pos_counter)
                    # [pos,ref,depth,countA,countC,countG,countT,perA..,perT]
                    filter_per = filter_data(per_data)
                    filter_per.insert(0, locus)
                    aln_info_writer.writerow(filter_per)
                    filter_per.insert(0, sample)
                    filter_per.insert(4, " ")
                    final_data = filter_per[:6] + filter_per[-5:]
                    # add info about this batch
                    final_data.append(sample_dir)
                    csv_writer.writerow(final_data)
                pos_counter += 1

print "done"
outfile.close()
