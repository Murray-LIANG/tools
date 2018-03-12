from __future__ import division

import itertools
import math
import sys
from functools import wraps
from multiprocessing import dummy as multithread
from time import time

# import mock
import storops
from tooz import coordination

unity = storops.UnitySystem('10.245.101.39', 'admin', 'Password123!')
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


def prepare_host_luns():
    hosts = [host for host in unity.get_host()
             if host.get_id() in ('Host_147', 'Host_148', 'Host_149',
                                  'Host_150', 'Host_166')]
    luns = [lun for lun in unity.get_lun()
            if lun.get_id() not in ('sv_999', 'sv_1061', 'sv_1062')]
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


@timing
def attach(host, lun):
    # with mock.patch('storops.unity.resource.host.UnityHost.attach',
    #                 new=fake_attach):
    #     host.attach(lun)
    host.attach(lun, skip_hlu_0=True)


def main(action):
    host_lun_pairs = prepare_host_luns()
    print('Number of host-lun pairs: {}'.format(len(host_lun_pairs)))
    pool = multithread.Pool(10)
    if action == 'test':
        coordinator = coordination.get_coordinator('file:///tmp/skip_hlu_0',
                                                   'localhost')
        coordinator.start()
        # pool.map(lambda t: attach_lock(coordinator, *t), host_lun_pairs)
        pool.map(lambda t: attach(*t), host_lun_pairs)
        coordinator.stop()
    elif action == 'clean':
        pool.map(lambda t: t[1].detach_from(None), host_lun_pairs)


if __name__ == '__main__':
    main(sys.argv[1])
