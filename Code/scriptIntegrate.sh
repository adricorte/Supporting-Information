#!/bin/bash
FILE1="$1"
BASENAME="$2"
EXTENSION="$3"
head -1 ${FILE1} > ${BASENAME}.${EXTENSION} 

tail -n +2 -q ${BASENAME}_*.${EXTENSION} >> ${BASENAME}.${EXTENSION} 
