#!/bin/bash


while read f; do
  echo $pair1 $pair2
  pair1=$(echo "$f" | cut -d$'\t' -f2)
  pair2=$(echo "$f" | cut -d$'\t' -f1)
  python ./genotyper_iter.py $pair1 $pair2
done <pairs.txt
