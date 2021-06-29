#!/bin/bash

python ./../../deepccs_prep.py 

cd ./../../../tools/deepccs/DeepCCS/interface/

DeepCCS predict -i ./../../../../Predictions_datasets/$1/deepccs/datadeepccs_corrected.csv -o ./../../../../Predictions_datasets/$1/deepccs/resultsdeepccs_raw.csv 

cd ./../../../../Predictions_datasets/$1/deepccs/

python ./../../deepccs_prep_results.py 

python ./../../create_report.py deepccs $1 $2 ./resultsdeepccs.csv

cat reportdeepccs.txt