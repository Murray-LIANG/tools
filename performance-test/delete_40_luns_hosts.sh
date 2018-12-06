#!/usr/bin/env bash

ospt_cmd='ospt --storops_unity 10.245.83.243 --username admin --password Password123!'

log_dir="${1:-$(date +'%Y%m%d_%H%M%S')}"

set -x

mkdir -p "${log_dir}"

$ospt_cmd --log $log_dir/delete-volumes.log delete-volumes --tag liangr --count 40 \
&& $ospt_cmd --log $log_dir/delete-servers.log delete-servers --tag liangr --count 40 
set +x
