#!/bin/bash

python ./../../create_report.py allccs $1 $2 ./resultsallccs.csv

cat reportallccs.txt
