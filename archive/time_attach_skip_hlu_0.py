from __future__ import division

import itertools
import math
import sys
from contextlib import contextmanager
from functools import wraps
from multiprocessing import dummy as multithread
from time import time

import storops

storops.enable_log()


def timing(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print('func:{} args:[{}, {}], time: {:.4f},{:.4f},{:.4f}'.format(
            f.__name__, [to_str(each) for each in args], kwargs, ts, te,
            te - ts))
        return result

    return wrap


def to_str(obj):
    if (isinstance(obj, storops.unity.resource.host.UnityHost)
            or isinstance(obj, storops.unity.resource.lun.UnityLun)):
        return obj.get_id()
    return str(obj)


@contextmanager
def timer():
    class _Time(object):
        def __init__(self, time_start):
            self.start = time_start
            self.end = None

        @property
        def interval(self):
            return self.end - self.start

    _timer = _Time(time())
    try:
        yield _timer
    finally:
        _timer.end = time()


def get_host_luns(array):
    if isinstance(array, storops.VNXSystem):
        hosts = sorted([host for host in array.get_sg()
                        if host.name.startswith('host-liangr-')],
                       key=lambda x: x.name)
        luns = sorted([lun for lun in array.get_lun()
                       if lun.name.startswith('vol-liangr-')],
                      key=lambda x: x.name)
    else:
        hosts = sorted([host for host in array.get_host()
                        if host.name.startswith('host-liangr-')],
                       key=lambda x: x.get_id())
        luns = sorted([lun for lun in array.get_lun()
                       if lun.name.startswith('vol-liangr-')],
                      key=lambda x: x.get_id())

    n = int(math.ceil(len(luns) / len(hosts)))
    hosts_repeat = itertools.chain.from_iterable([hosts] * n)
    return zip(hosts_repeat, luns)


def fake_attach(*args):
    print('Fake `attach` running.')


@timing
def attach_lock(coordinator, host, lun):
    lock = coordinator.get_lock(host.name)
    with lock():
        # with mock.patch('storops.unity.resource.host.UnityHost.attach',
        #                 new=fake_attach):
        #     host.attach(lun)
        host.attach(lun, skip_hlu_0=True)


def attach(array, index, host, lun):
    print('Attaching: {},{}'.format(host.name, lun.name))
    # import time as t
    # t.sleep(index * 2)
    with timer() as t:
        # with mock.patch('storops.unity.resource.host.UnityHost.attach',
        #                 new=fake_attach):
        #     host.attach(lun)
        if isinstance(array, storops.VNXSystem):
            host.attach_alu(lun)
        else:
            host.attach(lun, skip_hlu_0=True)
    print('Attached: {},{},{}'.format(host.name, lun.name, t.interval))


def detach(array, index, host, lun):
    print('Detaching: {},{}'.format(host.name, lun.name))
    import time as t
    t.sleep(index * 2)
    with timer() as t:
        if isinstance(array, storops.VNXSystem):
            host.detach_alu(lun)
        else:
            lun.detach_from(None)
    print('Detached: {},{},{}'.format(host.name, lun.name, t.interval))


def main(array, action, number=10):
    if array == 'vnx':
        array = storops.VNXSystem('192.168.1.50', 'sysadmin', 'sysadmin')
    else:
        array = storops.UnitySystem('10.245.187.16', 'admin', 'Password123!')
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
