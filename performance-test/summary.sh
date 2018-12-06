#!/bin/bash

set -x

folders="$@"

source ./utils.sh

summary="summary_$(date +'%Y%m%d_%H%M%S')"
mkdir -p ${summary}

for act in create-volumes delete-volumes attach detach; do
    for num in ${concurrencies}; do
        awk_cmd=''
        for dir in ${folders}; do
            awk_cmd+="<(awk '{ print \$NF }' ${dir}/${act}-${num}.csv) "
        done
        bash -c "paste ${awk_cmd} > ${summary}/${act}-${num}.csv"
        sed -i '1c'"${folders// /	}" ${summary}/${act}-${num}.csv
    done
done
set +x
