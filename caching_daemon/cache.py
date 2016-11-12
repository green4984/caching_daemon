# -*- coding: utf-8 -*-
from __future__ import absolute_import
import functools
import threading
from .storage import (BaseStorage, ThreadLocalStorage)

__all__ = (
    'cached',
)

__lock = threading.RLock()
__caches = None


def get_caches(storage=None):
    """

    :rtype: BaseStorage
    """
    global __caches
    global __lock
    if __caches:
        return __caches
    with __lock:
        if __caches:
            return __caches
        if storage:
            assert isinstance(storage, BaseStorage)
            __caches = storage
        else:
            __caches = ThreadLocalStorage()
    return __caches


def cached(timeout=10):
    def _wrapper(func):
        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            caches = get_caches()
            _id = func.func_name + func.func_code.co_filename + str(func.func_code.co_firstlineno)
            ms = timeout * 1000
            value = caches.get(_id)
            if value is not None:
                return value
            result = func(*args, **kwargs)
            caches.set(_id, result, ms)
            return result

        return _wrapped

    return _wrapper


def register_cached_function(timeout=10, args_callback=None, kwargs_callback=None):
    def _wrapper(func):
        @functools.wraps(func)
        def _wrapped(*args, **kwargs):
            caches = get_caches()
            _id = func.func_name + func.func_code.co_filename + str(func.func_code.co_firstlineno)
            ms = timeout * 1000
            value = caches.get(_id)
            if value is None:
                value = func(*args, **kwargs)
                caches.set(_id, value, ms)
            return value

        return _wrapped

    return _wrapper
