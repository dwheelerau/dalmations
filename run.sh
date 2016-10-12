#!/usr/bin/env bash

#######
##
##
##
##
#######

ref=./reference_mlst/mlst
# alg left and right reads to different sam files

bowtie2 -x $ref -U ZWF1bpft.fastq.trimmed -S l.sam
bowtie2 -x $ref -U ZWF1bprt.fastq.trimmed -S r.sam

samtools view -Sb l.sam | samtools sort - l.sorted
samtools view -Sb r.sam | samtools sort - r.sorted

samtools index l.sorted.bam
samtools index r.sorted.bam

# target region seems to require this or output is strange
locus=ZWF1b

/home/dwheeler/software_tools/bam-readcount-master/bin/bam-readcount \
    --max-warnings 0 \
    -f $ref.fa l.sorted.bam $locus | \
    cut -f1,2,3,4,6-9  > table.forward.txt
/home/dwheeler/software_tools/bam-readcount-master/bin/bam-readcount \
    --max-warnings 0 \
    -f $ref.fa r.sorted.bam $locus | \
    cut -f1,2,3,4,6-9 > table.reverse.txt

python process_tables.py

#filter cols
python filter_cols.py
