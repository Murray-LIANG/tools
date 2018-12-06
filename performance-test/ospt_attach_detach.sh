#!/usr/bin/env bash

ospt_cmd='ospt --storops_unity 10.245.83.243 --username admin --password Password123!'

log_dir="${1:-$(date +'%Y%m%d_%H%M%S')}"

set -x

mkdir -p "${log_dir}"

for num in 10 20 30 40; do
    for i in {1..3}; do
        $ospt_cmd --log $log_dir/attach-$num-$i.log attach --tag liangr --count $num \
        && $ospt_cmd --log $log_dir/detach-$num-$i.log detach --tag liangr --count $num
    done
done
set +x
