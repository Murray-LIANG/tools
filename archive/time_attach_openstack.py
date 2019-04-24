from __future__ import division

import itertools
import math
import sys
from contextlib import contextmanager
from functools import wraps
from multiprocessing import dummy as multithread
import time

import storops

from novaclient import client as n_client
from cinderclient import client as c_client
from glanceclient import client as g_client


@contextmanager
def timer():
    class _Time(object):
        def __init__(self, time_start):
            self.start = time_start
            self.end = None

        @property
        def interval(self):
            return self.end - self.start

    _timer = _Time(time.time())
    try:
        yield _timer
    finally:
        _timer.end = time.time()


class TimeOutException(Exception):
    pass


CRED = {
    'username': 'admin',
    'api_key': 'welcome',
    'auth_url': 'http://192.168.77.34:5000/v2.0',
    'project_id': 'admin'
}

NOVA = n_client.Client(1.1, **CRED)
CINDER = c_client.Client(2, **CRED)
GLANCE = g_client.Client(1, **CRED)

NAME_TAG = 'ml-test'


def wait_until(client, res_id, criteria, timeout=60):
    start_point = time.time()
    while True:
        if time.time() - start_point > timeout:
            raise TimeOutException(
                'Timeout before {} becoming {}. {} sec passed.'.format(
                    res_id, criteria, timeout))
        time.sleep(1)
        res = client.get(res_id)
        if res.status == criteria:
            break


def create_volume(index):
    name = 'vol-{}-{:02d}'.format(NAME_TAG, index)
    print('Creating volume: {}.'.format(name))
    time.sleep(index * 2)
    with timer() as t:
        v = CINDER.volumes.create(name=name, size=5)
        wait_until(CINDER, v.id, 'available')
    print('Created volume: {},{}'.format(name, t.interval))


def delete_volume(volume):
    volume.delete()


def create_server(index):
    image = [each for each in GLANCE.images.list()
             if each.name.startswith('cirros')][0]
    flavor = NOVA.flavors.get(1)
    name = 'vm-{}-{:02d}'.format(NAME_TAG, index)
    print('Creating vm: {}.'.format(name))
    vm = NOVA.servers.create(name=name, image=image, flavor=flavor)
    wait_until(NOVA, vm.id, 'running')
    print('Created vm: {},{}'.format(name, vm.interval))


def delete_server(server):
    server.delete()


def attach_volume(server_id, volume_id):
    print('Attaching: {},{}.'.format(server_id, volume_id))
    with timer() as t:
        NOVA.volumes.create_server_volume(server_id, volume_id)
        wait_until(CINDER, volume_id, 'in-use')
    print('Attached: {},{},{}'.format(server_id, volume_id, t.interval))


def detach_volume(server_id, volume_id=None):
    NOVA.volumes.delete_server_volume(server_id, volume_id)


def get_servers_volumes():
    servers = [each for each in NOVA.servers.list() if NAME_TAG in each.name]
    volumes = [each for each in CINDER.volumes.list() if NAME_TAG in each.name]

    # n = int(math.ceil(len(volumes) / len(servers)))
    # servers_repeat = itertools.chain.from_iterable([servers] * n)
    return zip(servers, volumes)


def main(action):
    if action == 'create-volumes':
        pass
    elif action == 'clean-volumes':
        pass
    elif action == 'create-servers':
        pass
    elif action == 'clean-servers':
        pass
    elif action == 'attach':
        pass
    elif action == 'detach':
        pass
    else:
        print('Nothing to do')
    host_lun_pairs = get_host_luns(array)

    pool = multithread.Pool(number)
    host_lun_pairs = host_lun_pairs[:number]
    print('Number of host-lun pairs: {}.'.format(number))
    with timer() as total_time:
        if action == 'test':
            # coordinator = coordination.get_coordinator(
            #     'file:///tmp/skip_hlu_0', 'localhost')
            # coordinator.start()
            # pool.map(lambda t: attach_lock(coordinator, *t), host_lun_pairs)
            pool.map(lambda t: attach(array, t[0], *t[1]),
                     enumerate(host_lun_pairs))
            # coordinator.stop()
        elif action == 'clean':
            pool.map(lambda t: detach(array, t[0], *t[1]),
                     enumerate(host_lun_pairs))
        elif action == 'clean-dummylun':
            dummy_luns = [lun for lun in array.get_lun()
                          if lun.name.startswith('storops_dummy_lun')]
            pool.map(lambda t: t.delete(), dummy_luns)
    print('Total time: {}'.format(total_time.interval))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
