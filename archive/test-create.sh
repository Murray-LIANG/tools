#!/usr/bin/env bash

for num in 46; do
    for i in 1; do
        sleep 2
        python time_create.py test ${num} 2>&1 | \
            tee hujun-create-lun-${num}-${i}.log
        #&& python time_create.py clean ${num} 2>&1 > /dev/null
    done
done
