#!/usr/bin/env bash

for num in 10; do
    for i in 3; do
        sleep 2
        python time_attach_skip_hlu_0.py test ${num} 2>&1 | \
            tee harrier-${num}-luns-per-host-${i}-attaching.log \
        && python time_attach_skip_hlu_0.py clean ${num} 2>&1 > /dev/null
    done
done
