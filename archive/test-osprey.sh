#!/usr/bin/env bash

for num in 10 15 25 30 40; do
    for i in {1..3}; do
        sleep 10
        python time_attach_skip_hlu_0.py test ${num} 2>&1 | \
            tee attach-modify-hlu-osprey-${num}-${i}.log \
        && python time_attach_skip_hlu_0.py clean ${num} 2>&1 > /dev/null
    done
done