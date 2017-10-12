#!/bin/bash
dirr=$PWD
for U in 4.2 4.4 4.6 4.8 5; do
  for R in 3 4; do
    for dir in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do
      cd $dirr/U$U/R$R/$dir/rawdata
      python $dirr/prebin.py
    done
  done
done
