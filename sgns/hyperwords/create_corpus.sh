#!/usr/bin/env bash

for i in {1810..2000..10}
  do 
     bash corpus2sgns.sh --cds 0.75 --win 5 --neg 15 --dim 300 --thr 5 ../../coha-decades-new/coha.${i}s output/${i}
 done
