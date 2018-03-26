#!/usr/bin/env bash

for num in 10 15 20 25 30 40; do
    for i in {1..3}; do
        sleep 2
        python time_attach_skip_hlu_0.py test ${num} 2>&1 | \
            tee peter-1-lun-per-host-${num}-${i}-dummy-lun.log \
        && python time_attach_skip_hlu_0.py clean ${num} 2>&1 > /dev/null
    done
    python time_attach_skip_hlu_0.py clean-dummylun ${num} 2>&1 > /dev/null
done
