#!/bin/bash


darkchem predict prop ./datadarkchem.tsv ./../../../tools/darkChem/darkchem-weights/deprotonated/
mv datadarkchem_darkchem.tsv resultsdarkchem_deprotonated.tsv
darkchem predict prop ./datadarkchem.tsv ./../../../tools/darkChem/darkchem-weights/protonated/
mv datadarkchem_darkchem.tsv resultsdarkchem_protonated.tsv
darkchem predict prop ./datadarkchem.tsv ./../../../tools/darkChem/darkchem-weights/sodiated/
mv datadarkchem_darkchem.tsv resultsdarkchem_sodiated.tsv

python ./../../darkchem.py resultsdarkchem_deprotonated.tsv resultsdarkchem_protonated.tsv resultsdarkchem_sodiated.tsv

python ./../../create_report.py darkchem $1 $2 ./resultsdarkchem.csv

cat reportdarkchem.txt