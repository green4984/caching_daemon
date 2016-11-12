# -*- coding: utf-8 -*-
from abc import abstractmethod
import threading
import time


class BaseStorage(object):
    def __init__(self, uri=None):
        self.uri = uri

    @staticmethod
    def current_timestamp():
        return int(time.time() * 1000)

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def set(self, key, value, timeout):
        pass


class ThreadLocalStorage(BaseStorage):
    def __init__(self):
        self.local = threading.local()
        super(ThreadLocalStorage, self).__init__()

    def get(self, key):
        store = getattr(self.local, key, None)
        if not store:
            return None
        if 'expire' not in store:
            return store.get('data')
        expire = store.get('expire')
        curr = ThreadLocalStorage.current_timestamp()
        timespan = store.get('timespan', 0)
        if 0 <= expire - curr <= timespan:
            return store.get('data')
        delattr(self.local, key)
        return None

    def set(self, key, value, timeout):
        if int(timeout) <= 0:
            data = {'data': value}
        else:
            data = {
                'expire': ThreadLocalStorage.current_timestamp() + timeout,
                'data': value,
                'timespan': timeout
            }
        setattr(self.local, key, data)