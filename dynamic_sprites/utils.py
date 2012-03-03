# -*- coding: utf-8 -*-

from functools import wraps


def cached_property(fn):
    @wraps(fn)
    def wrapper(self):
        cache_var = '_%s' % fn.__name__
        if not hasattr(self, cache_var):
            setattr(self, cache_var, fn(self))
        return getattr(self, cache_var)
    return property(wrapper)
