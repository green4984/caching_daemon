# -*- coding: utf-8 -*-

import time
import random
import caching_daemon


@caching_daemon.cached(timeout=0.1)
def test(a):
    return a


@caching_daemon.cached(timeout=1)
def test2(a):
    return random.randrange(1, 10)


class Test(object):
    def __init__(self):
        pass

    @caching_daemon.cached(timeout=1)
    def test(self):
        return random.randrange(1, 100)

if __name__ == '__main__':
    t = Test()
    for i in xrange(1, 100):
        print "%d %d" % (t.test(), t.test())
        time.sleep(0.1)
