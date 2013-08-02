#!/bin/bash

#$ -N TBEEF
#$ -q mathbio5
#$ -m bea

module load python/3.2.2
module load R/3.0.1
python3 driver.py
