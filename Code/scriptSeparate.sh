#!/bin/bash
FILENAME="$1"
HDR=$(head -1 ${FILENAME})
NOEXTENSION=$(echo "$FILENAME" | cut -f 1 -d '.')
split -l $2 ${FILENAME} xyz
n=1
for f in xyz*
do
    if [[ ${n} -ne 1 ]]; then
        echo ${HDR} > ${NOEXTENSION}_part_${n}.csv
    fi
    cat ${f} >> ${NOEXTENSION}_part_${n}.csv
    rm ${f}
    ((n++))
done