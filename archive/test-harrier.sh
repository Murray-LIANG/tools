#!/usr/bin/env bash

for num in 10 15 20 25 30 40; do
    for i in 1; do
        sleep 2
        python time_attach_skip_hlu_0.py unity test ${num} 2>&1 | \
            tee james-before-release-full-concurrency-${num}-${i}.log \
        && python time_attach_skip_hlu_0.py unity clean ${num} 2>&1 > /dev/null
    done
    #python time_attach_skip_hlu_0.py clean-dummylun ${num} 2>&1 > /dev/null
done
