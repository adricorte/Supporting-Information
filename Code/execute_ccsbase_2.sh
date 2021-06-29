#!/bin/bash

bash ./../../scriptIntegrate.sh resultsccsbase_part_1.csv resultsccsbase csv 

python ./../../create_report.py ccsbase $1 $2 ./resultsccsbase.csv

cat reportccsbase.txt
