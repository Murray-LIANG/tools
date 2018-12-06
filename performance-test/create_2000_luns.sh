#!/bin/bash

csrf_token=$(curl -k -i -s -c ./cookies.txt -L -u admin:Password123! \
    --header "X-EMC-REST-CLIENT:true" \
    "https://10.245.83.243/api/types/user/instances" \
    | sed -n 's/^EMC-CSRF-TOKEN: \(.*\)/\1/p' | tr -d '\r')

[ -z $csrf_token ] && { echo "failed to get csrf token"; exit 1; }

echo "##### Got EMC-CSRF-TOKEN: $csrf_token"

mkdir -p ./req_body

for i in {0..19}; do
    sed 's/lun_prefix/lun-'$i'/g' < req_create_100_luns.template \
        > ./req_body/req_create_100_luns_$i.json && \
        curl -k -i -s -c ./cookies.txt -b ./cookies.txt \
            --header "X-EMC-REST-CLIENT:true" \
            --header "Content-Type:application/json" \
            --header "Accept:application/json" \
            --header "EMC-CSRF-TOKEN:$csrf_token" -u admin:Password123! \
            --data "@req_body/req_create_100_luns_$i.json" -X POST \
            'https://10.245.83.243/api/types/job/instances?compact=true&visibility=Engineering&timeout=-1'
done

