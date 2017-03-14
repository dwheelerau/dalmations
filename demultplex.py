import sys
import os

# usage:
# python demultplex.py 12-0039_S10_L001_R2_001.fastq \
# forward_primers.txt reverse_primers.txt | tee -a log.txt

filein=sys.argv[1] # In my case, the name of the file to be demultiplexed was in the format [Sample]_[SampleNumber]_L001_R1_001.fastq, e.g. N1B_S17_L001_R1_001.fastq
barcodes_forward=sys.argv[2] #forward barcodes
barcodes_rev=sys.argv[3] #reverse barcodes
os.system('mkdir %s_%s'%(filein.split('_')[0],filein.split('_')[1])) #Create output folder for demultiplexed files

# Run fastx splitter
if 'L001_R1_001' in filein:
	os.system('cat %s | fastx_barcode_splitter.pl --bcfile %s --bol --mismatches 2 --prefix %s_%s/%s- --suffix "_L001_R1_001.fastq"'%(filein, barcodes_forward, filein.split('_')[0],filein.split('_')[1],filein.split('_')[1]))
elif 'L001_R2_001' in filein:
	os.system('cat %s | fastx_barcode_splitter.pl --bcfile %s --bol --mismatches 2 --prefix %s_%s/%s- --suffix "_L001_R2_001.fastq"'%(filein, barcodes_rev, filein.split('_')[0],filein.split('_')[1],filein.split('_')[1]))




'''
Example barcode file:

AAT1aprt TCAAGAAATCAGCGATAACT
ACC1prt GTGGAATGCTCGGTTTTAGA
ADP1prt CTTTGTTCTTACCAGCCAAA
MPIprt TGCTTCCCCTTTGTTCAAAC
SYA1prt ACAGCTTTAGCCAACTCATT
VPS13prt CCCATGATTTGATTCCAGTT
ZWF1bprt TTAGCTGGATCTTCAACGGC


All tags must be same length.
'''
