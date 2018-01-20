# var_scanner

## Introduction  
Multi-locus sequence typing (MLST) is a highly discriminating *Candida albicans* strain typing method. It is usually applied to one colony per patient sample. However, multiple strains can coexist in the same site in a patient. We therefore developed 100+1 NGS-MLST (var_scanner), a next generation sequencing (NGS) modification of the existing *C. albicans* MLST method. It analyzes DNA extracted from a pool of 100 colonies from a sample plus DNA from one colony and bioinformatically infers the genotypes present and their frequency. It does so at a sequencing cost, per patient sample, four times lower than that of conventional MLST.  For the directly typed single colonies its discriminating power is 0.998, comparable to that of conventional MLST. Its predictions of the ratio of different strains in a sample were fairly accurate - within 14±16% of the ratio between the numbers of colonies from two known strains combined to generate DNA pools for testing the method’s accuracy.  

Details of our proof of principle experiment using 100+1 NGS-MLST can be found in the our recent publication XXXX.

To cite var_scanner:
XXXX *et al*:DIO:XXXXX  

## Requirements  
This software has been tested on Ubuntu 14.04 and 16.06. This scripts are written in pure python and only require python 2.7 installed on the machine. The software may run on Mac and windows as long as python 2.7 is installed, but this has not been tested.


## Installation  
Create a base directory and clone the repo into.  
```bash
git clone git@github.com:dwheelerau/var_scanner.git
cd var_scanner
```

# setup the directories
```bash
mkdir final_genotypes/
mkdir final_sequences/
mkdir final_results/
mkdir genotype_data/
mkdir samples/
```

## File and folder/structure required  
The following file/folder structure is required to run var_scanner. These should exist if you followed the installion instructions shown above:  
<pre>
BASE_DIR--samples--sample1_data
                 --sample2_data
                 --sample...
        --final_genotpyes 
        --final_sequences 
        --genotype_data  
        --reference_mlst--mlst.fa
        --reate_sequences.py  
        --extract_seq_from_sheet.py 
        --run_aligner.py  
        --demultplex.py  
        --genotyper_iter.py 
</pre>

## Running var_scanner (gui version)
The GUI is under current development (see github branch). Stay tuned.....

## Running var_scanner (non-gui version)

1. Either use the included demultplex.py script to demultplex your samples into the `samples` directory (in this case the BASE DIRECTORY is called var_scanner), with the child directories named after the sample. For example, a sample called `1161NK_S75`, which was sequenced using the 7 MLST primer combinations in paired end mode (ft = R1 and rt = R2), would have the following folder/file structure.  
<pre>
var_scanner/samples/1161NK_S75/AAT1apft.fastq  
var_scanner/samples/1161NK_S75/AAT1aprt.fastq  
var_scanner/samples/1161NK_S75/SYA1pft.fastq  
var_scanner/samples/1161NK_S75/SYA1prt.fastq  
var_scanner/samples/1161NK_S75/ACC1pft.fastq  
var_scanner/samples/1161NK_S75/ACC1prt.fastq   
var_scanner/samples/1161NK_S75/VPS13pft.fastq  
var_scanner/samples/1161NK_S75/VPS13prt.fastq   
var_scanner/samples/1161NK_S75/ADP1pft.fastq  
var_scanner/samples/1161NK_S75/ADP1prt.fastq   
var_scanner/samples/1161NK_S75/ZWF1bpft.fastq  
var_scanner/samples/1161NK_S75/ZWF1bprt.fastq  
var_scanner/samples/1161NK_S75/MPIpft.fastq    
var_scanner/samples/1161NK_S75/MPIprt.fastq
</pre>

If sequences need demultiplexing then run the `demultiplex.py` using the following command:   

```bash
usage:  
    python2 demultplex.py 12-0039_S10_L001_R2_001.fastq \
        forward_primers.txt reverse_primers.txt | tee -a log.txt
```

The `forward_primers.txt` and `reverse_primers.txt` files are included in this repo.  

2.  Run the `run_aligner.py` script.  

```bash
usage:
    python2 run_aligner.py samples/
```
If the above script works correctly each of the sample folders should now contain files ending in `.aln`, `.csv`, `.data`. The final table of genotype frequencies should be found in the `final_results` directory in a file called `final_table_python.csv`.   

3.  Run the `genotyper_iter.py` script.  

In the example below, SINGLE_COLONY_NAME and MIX_COLONY_NAME would correspond to sample folders found in the sample directory; they should also be found in the first column of the `final_table_python.csv`.  

```bash
usage:
    python2 genotyper_iter.py <SINGLE_COLONY_NAME> <MIX_COLONY_NAME>  

example:
    python2 genotyper_iter.py FJ9-S_S16 P1-50-50_S35    
```

For convenience, if you have multiple pairs that you would like to process, place the pairs into a tab-separated text file, as follows:
<pre>
SINGLE_COLONY_NAME1     MIX_COLONY_NAME1
SINGLE_COLONY_NAME2     MIX_COLONY_NAME2
SINGLE_COLONY_NAME3     MIX_COLONY_NAME3
</pre>

Then process these automatically using the included shell script `run_genotyper.sh` using the following command:

```bash
./run_genotyper.sh pair.txt
```

Where `pair.txt` repressents the tab-separated file that you saved the pairs.

4.  Run the `create_sequences.py` script to generate the derived MLST sequence for each sample.  

```bash
usage:
    python2 create_sequences.py
```
The final sequence file is saved in `final_sequences/sequences.fa`.  

## Important output files  
* `final_sequences/sequences.fa` which contains the dervied single and mix colony concatinated MLST sequences. These sequences can be compared to previous results using alignments or via phylogenetic trees.  

* `final_results/final_table_python.csv` the allele calls for each sample  
* `genotype_data/*.csv` comma separated file containing XXXXX (pairs)  
* `final_genotypes/*.csv` comma separated file containing XXXXX (pairs)  
* `samples/SAMPLENAME/SAMPLENAME.aln` XXXXX  
* `samples/SAMPLENAME/SAMPLENAME.aln_data` XXXXX  
* `samples/SAMPLENAME/SAMPLENAME.aln_info.csv` XXXXX  

## Disclaimer
This is free software and is provided with no warranty what-so-ever.

        
