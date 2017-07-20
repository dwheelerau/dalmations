# var_scanner

## Introduction  
Multi-locus sequence typing (MLST) is a highly discriminating *Candida albicans* strain typing method. It is usually applied to one colony per patient sample. However, multiple strains can coexist in the same site in a patient. We therefore developed 100+1 NGS-MLST (var_scanner), a next generation sequencing (NGS) modification of the existing *C. albicans* MLST method. It analyzes DNA extracted from a pool of 100 colonies from a sample plus DNA from one colony and bioinformatically infers the genotypes present and their frequency. It does so at a sequencing cost, per patient sample, four times lower than that of conventional MLST.  For the directly typed single colonies its discriminating power is 0.998, comparable to that of conventional MLST. Its predictions of the ratio of different strains in a sample were fairly accurate - within 14±16% of the ratio between the numbers of colonies from two known strains combined to generate DNA pools for testing the method’s accuracy.  

Details of our proof of principle experiment using 100+1 NGS-MLST can be found in the our recent publication XXXX.

To cite var_scanner:
XXXX *et al*:DIO:XXXXX  

## Requirements  
This software has been tested on Ubuntu 14.04 and 16.06. This scripts are writen in pure python and only require python 2.7 installed on the machine. The software should also run on Mac and windows computers (using cygwin) as long as python 2.7 is installed (but this has not been tested).


## Installation  
Create a base directory and clone the repo into.  
```bash
mkdir var_scanner && cd var_scanner   
git clone XXXXX   
```

# setup the directories
```bash
mkdir final_genotypes/
mkdir final_sequences/
mkdir genotype_data/
```

## File and folder/structure required  
The following file/folder structure is required to run var_scanner. These should exist if you followed the installion instructions shown above:  
<pre>
BASE_DIR/samples/  # contains demultiplexed samples in directories named after the sample name
        /final_genotpyes/  # data Xxxx
        /final_sequences/ # data xxx
        /genotype_data/  # data xxx
        /reference_mlst/  # reference MLST sequence used for alignment
        /create_sequences.py  # script to create infered fasta files for alignment
        /extract_seq_from_sheet.py  # script to extract sequences from data sheet
        /run_aligner.py  # alignment script
        /demultplex.py  # demultiplex script that saves sequence files in folders named after the sample names
        /genotyper_iter.py  # genotyper script
</pre>

## Running var_scanner (gui version)
The GUI is under current development. Stay tuned..

## Running var_scanner (non-gui version)

1. Either use the included demultplex.py script to demultplex your samples into directories named after the sample and place these in the BASE_DIR/sample_name/MLST_name.fastq directory. This would be an example for a sample called `1161NK_S75`, which was sequenced using the 7 MLST primer combinations in paired end mode (ft = R1 and rt = R2).  
<pre>
BASE_DIR/samples/1161NK_S75/AAT1apft.fastq  
BASE_DIR/samples/1161NK_S75/AAT1aprt.fastq  
BASE_DIR/samples/1161NK_S75/SYA1pft.fastq  
BASE_DIR/samples/1161NK_S75/SYA1prt.fastq  
BASE_DIR/samples/1161NK_S75/ACC1pft.fastq  
BASE_DIR/samples/1161NK_S75/ACC1prt.fastq   
BASE_DIR/samples/1161NK_S75/VPS13pft.fastq  
BASE_DIR/samples/1161NK_S75/VPS13prt.fastq   
BASE_DIR/samples/1161NK_S75/ADP1pft.fastq  
BASE_DIR/samples/1161NK_S75/ADP1prt.fastq   
BASE_DIR/samples/1161NK_S75/ZWF1bpft.fastq  
BASE_DIR/samples/1161NK_S75/ZWF1bprt.fastq  
BASE_DIR/samples/1161NK_S75/MPIpft.fastq    
BASE_DIR/samples/1161NK_S75/MPIprt.fastq
</pre>

If sequences need demultiplexing then run the `demultiplex.py` using the following command:   

```bash
usage:  
    python demultplex.py 12-0039_S10_L001_R2_001.fastq \
        forward_primers.txt reverse_primers.txt | tee -a log.txt
```

The `forward_primers.txt` and `reverse_primers.txt` files are included in this repo.  
**TODO: check primers are in the repo**

2.  Run the `run_aligner.py` script (assuming the samples to analyse are saved in the samples directory.  

```bash
usage:
    python run_aligner.py <samples>
    
example:
    python run_aligner.py samples
```
If the above script works correctly each of the sample folders should now contain files ending in `.aln`, `.csv`, `.data`. The final table of genotype frequencies should be found in the `final_results` directory in a file called `final_table_python.csv`.   

3.  Run the `genotyper_iter.py` script.  

In the example below, SINGLE_COLONY_NAME and MIX_COLONY_NAME would correspond to sample folders found in the sample directory; they should also be found in the first column of the `final_table_python.csv`.  

```bash
usage:
    python genotyper_iter.py <SINGLE_COLONY_NAME> <MIX_COLONY_NAME>  

example:
    python genotyper_iter.py FJ9-S_S16 P1-50-50_S35    
```

4.  Run the `create_sequences.py` script to generate the derived MLST sequence for each sample.  
The final sequence file is saved in `final_sequences/sequences.fa`.  

```bash
usage:
    python create_sequences.py
```


## Disclaimer
This is free software and is provided with no warranty what-so-ever.

        
