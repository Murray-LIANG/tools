#!/usr/bin/env bash

for num in 10 15 20 25 30 40; do
    for i in {1..3}; do
        sleep 2
        python time_attach_skip_hlu_0.py vnx test ${num} 2>&1 | \
            tee vnx-${num}-${i}.log \
        && python time_attach_skip_hlu_0.py vnx clean ${num} 2>&1 > /dev/null
    done
done
