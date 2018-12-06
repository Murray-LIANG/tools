#!/usr/bin/env bash

set -x

source ./utils.sh


#
# Performance test on creating/deleting volumes
#
sleep 60

pt_create_delete


#
# Prepare luns and hosts for attach/detach test
#
prepare_luns_hosts


#
# Performance test on attaching/detaching
#
sleep 60

pt_attach_detach


#
# Clean up luns and hosts for attach/detach test
#
cleanup_luns_hosts


#
# Collect the time
#
collect_time


set +x

echo "ALL DONE"
