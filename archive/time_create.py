from __future__ import division

import itertools
import math
import sys
from contextlib import contextmanager
from functools import wraps
from multiprocessing import dummy as multithread
from time import time

import storops

unity = storops.UnitySystem('10.245.101.114', 'admin', 'Password123!')
storops.enable_log()


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


def create_lun(index, pool, lun_name):
    import time as t
    t.sleep(index * 2)
    print('Creating: {},{}'.format(pool.name, lun_name))
    with timer() as t:
        pool.create_lun(lun_name)
    print('Created: {},{},{}'.format(pool.name, lun_name, t.interval))


def delete_lun(lun_name):
    lun = unity.get_lun(name=lun_name)
    print('Deleting: {}'.format(lun_name))
    lun.delete()
    print('Deleted: {}'.format(lun_name))


def main(action, number=10):
    unity_pool = unity.get_pool(name='pool-1')
    print('Using Pool: {}.'.format(unity_pool.name))

    lun_names = ['lun-liangr-{:02d}'.format(i) for i in range(number)]

    pool = multithread.Pool(number)
    with timer() as total_time:
        if action == 'test':
            pool.map(lambda t: create_lun(t[0], unity_pool, t[1]),
                     enumerate(lun_names))
        elif action == 'clean':
            pool.map(lambda t: delete_lun(t), lun_names)
    print('Total time: {}'.format(total_time.interval))


if __name__ == '__main__':
    main(sys.argv[1], int(sys.argv[2]))
