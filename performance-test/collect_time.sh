#!/usr/bin/env bash

dir=$1

set -x

cd $dir

#pattern='s/.*Thread-\([0-9]*\) .*TIME: \([0-9\.]*\),.*/\1\t\2/p'
pattern='s/.*TIME: \([0-9\.]*\),.*/\1/p'

for num in 10 20 30 40; do
    for act in create-volumes delete-volumes attach detach; do
        for i in {1..3}; do
            sed -n "${pattern}" $act-$num-$i.log > $act-$num-$i.time
        done
        paste $act-$num-*.time > $act-$num.time
	awk -v OFS='\t' '{ print $0,($1+$2+$3)/3 }' $act-$num.time > $act-$num.csv
        sed -i '1 i\Round #1\tRound #2\tRound #3\tAvg.' $act-$num.csv
    done
done

cd -

set +x
