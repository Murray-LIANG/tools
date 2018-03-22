#!/usr/bin/env python

import sys

import storops
import urllib3

urllib3.disable_warnings()

PY_NAME = sys.argv[0]

USAGE = '''
Usage: {py_name} <unity-ip> <user> <password> <hosts-txt>
    unity-ip: the Unity IP address.
    user: the user name to login the Unity.
    password: the password to login.
    host-txt: the txt file where stores host names one per line.
'''.format(py_name=PY_NAME)

if len(sys.argv) != 5:
    print(USAGE)
    exit(1)

UNITY_IP, USER_NAME, PASSWORD, HOSTS_TXT = sys.argv[1:]

with open(HOSTS_TXT, 'r') as f:
    all_host_names = [each.strip() for each in f.readlines()]

# the hosts in the same group share the same dummy lun.
# split all_host_names into sub-list
# ['host-0', 'host-1', ..., 'host-n'] ==>
#   [['host-0', ..., 'host-9'], ['host-10', ..., 'host-19'], ....]
hosts_group = [all_host_names[i:i + 10]
               for i in range(0, len(all_host_names), 10)]

DUMMY_LUN_PREFIX = 'storops_dummy_lun'
UNITY = storops.UnitySystem(UNITY_IP, USER_NAME, PASSWORD)


def _delete_lun(lun):
    print('>>> Deleting dummy lun: {}...'.format(lun.name))
    lun.delete()


def _create_host_if_not_exist(host_name):
    try:
        host = UNITY.get_host(name=host_name)
        print('>>> Host: {} exists...'.format(host_name))
    except storops.exception.UnityResourceNotFoundError:
        print('>>> Creating host: {}...'.format(host_name))
        host = UNITY.create_host(host_name)
    return host


# delete all dummy luns
print('>>> Deleting legacy dummy luns...')
map(_delete_lun,
    filter(lambda lun: lun.name.startswith(DUMMY_LUN_PREFIX), UNITY.get_lun()))

# always use the first pool got to create the dummy luns
POOL = UNITY.get_pool()[0]
all_hosts = []
for index, host_names in enumerate(hosts_group):
    hosts = list(map(_create_host_if_not_exist, host_names))
    all_hosts.extend(hosts)
    host_access = [{'host': host, 'accessMask': 1} for host in hosts]
    dummy_lun_name = '{}-{:03d}'.format(DUMMY_LUN_PREFIX, index)
    print('>>> Creating and attaching dummy lun: {}...'.format(dummy_lun_name))
    POOL.create_lun(lun_name=dummy_lun_name, host_access=host_access)

# some validation behind this line
print('>>> Doing final validation...')
if len(all_hosts) != len(all_host_names):
    print('>>> !!! The count of hosts mismatch {}!={}.'.format(
        len(all_hosts), len(all_host_names)))

for host in all_hosts:
    host.update()
    if not host.host_luns:
        print('>>> !!! The host: {} has no host LUN attached.'.format(
            host.name))
    for host_lun in host.host_luns:
        host_lun = storops.unity.resource.host.UnityHostLun.get(
            UNITY._cli, _id=host_lun.get_id())
        if host_lun.lun.name.startswith(DUMMY_LUN_PREFIX) \
                and host_lun.hlu != 0:
            print('>>> !!! The dummy lun: {} is attached to host: {}, but '
                  'with hlu {}.'.format(host_lun.lun.name, host.name,
                                        host_lun.hlu))



