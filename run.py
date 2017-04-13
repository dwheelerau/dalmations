#!/usr/bin/env python
import subprocess
import os
import csv

ref = "./reference_mlst/mlst"
sample_dir = "samples"

target_files = [('AAT1apft.fastq', 'AAT1aprt.fastq'),
                ('ACC1pft.fastq', 'ACC1prt.fastq'),
                ('ADP1pft.fastq', 'ADP1prt.fastq'),
                ('MPIpft.fastq', 'MPIprt.fastq'),
                ('SYA1pft.fastq', 'SYA1prt.fastq'),
                ('VPS13pft.fastq', 'VPS13prt.fastq'),
                ('ZWF1bpft.fastq', 'ZWF1bprt.fastq')]

sample_dirs = next(os.walk(sample_dir))[1]

# main commands
aln_cmd = "bowtie2 -x %s -U %s -S %s"  # ref, infile, outfile.sam
samtools1 = "samtools view -Sb %s > %s"  # in.sam , out.bam
samtools2 = "samtools sort %s %s"  # in.bam, out.sorted.bam
samtools3 = "samtools index %s"  # in.sorted.bam
readcount = '/home/dwheeler/software_tools/bam-readcount-master/bin/bam-readcount --max-warnings 0 -f reference_mlst/mlst.fa %s %s | cut -f1,2,3,4,6-9 > %s'
proctab = "python process_tables.py %s %s"
filttab = "python filter_cols.py %s %s"

# make a directory for final data
res = subprocess.check_output(['mkdir', '-p', 'final_results'])

# add header, close, then filter_cols.py will append to this
outfile = open('final_results/final_table.csv', 'w')
csv_writer = csv.writer(outfile)
csv_writer.writerow(['Sample', 'loci', 'pos', 'ref',
                     'read', 'depth', 'A_freq', 'C_freq',
                     'G_freq', 'T_freq', 'non_ref'])
# write header once then close off, will append results from filter_col.py
outfile.close()

for sample in sample_dirs:
    print sample
    for pair in target_files:
        outdir = "%s/%s/" % (sample_dir, sample)  # sample/DIR/

        # aln with bowtie
        targetf = outdir + pair[0]
        cmd3 = aln_cmd % (ref, targetf, targetf.split(".")[0]+".sam")
        res = subprocess.check_output(["bash", "-c", cmd3])
        targetr = outdir + pair[1]
        cmd4 = aln_cmd % (ref, targetr, targetr.split(".")[0]+".sam")
        res = subprocess.check_output(["bash", "-c", cmd4])

        # convert sam to bam
        cmd5 = samtools1 % (targetf.split(".")[0]+".sam",
                            targetf.split(".")[0]+".bam")
        res = subprocess.check_output(["bash", "-c", cmd5])
        cmd6 = samtools1 % (targetr.split(".")[0]+".sam",
                            targetr.split(".")[0]+".bam")
        res = subprocess.check_output(["bash", "-c", cmd6])

        # sort bam file
        cmd7 = samtools2 % (targetf.split(".")[0]+".bam",
                            targetf.split(".")[0]+".sorted")
        res = subprocess.check_output(["bash", "-c", cmd7])
        cmd8 = samtools2 % (targetr.split(".")[0]+".bam",
                            targetr.split(".")[0]+".sorted")
        res = subprocess.check_output(["bash", "-c", cmd8])

        # index bam files
        cmd9 = samtools3 % (targetf.split(".")[0]+".sorted.bam")
        res = subprocess.check_output(["bash", "-c", cmd9])
        cmd10 = samtools3 % (targetr.split(".")[0]+".sorted.bam")
        res = subprocess.check_output(["bash", "-c", cmd10])

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
