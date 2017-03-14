# var_scanner

If sequences need demultiplexing then run the demultiplex.py.

usage:
python demultplex.py 12-0039_S10_L001_R2_001.fastq \
  forward_primers.txt reverse_primers.txt | tee -a log.txt

I removed the len(14) for loop that only reported non-ref calls.
This was because we wanted all the tables to be the same number
of rows.
