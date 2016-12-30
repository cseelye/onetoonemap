#!/usr/bin/env python2.7
"""
A python module that implements a two-way mapping collection type
"""

from collections import MutableMapping

class TwoWayMap(MutableMapping):
    """
    Two-way mapping type. Objects of this type can be treated like a dict,
    except that both keys and values can be used to look each other up.
    d[k] -> v and d[v] -> k
    """

    def __init__(self, *args, **kwargs):
        self.__keymap = {}
        self.__valmap = {}
        self.update(*args, **kwargs)

    def __str__(self):
        return str(self.__keymap)

    def __repr__(self):
        return repr(self.__keymap)

    def __setitem__(self, k, v):
        self.__keymap[k] = v
        self.__valmap[v] = k

    def __getitem__(self, k):
        if k in self.__valmap:
            return self.__valmap[k]
        return self.__keymap[k]

    def get(self, k, default=None):
        return self.__keymap.get(k, self.__valmap.get(k, default))

    def __delitem__(self, k):
        v = self.__keymap[k]
        del self.__keymap[k]
        del self.__valmap[v]

    def __iter__(self):
        return iter(self.__keymap)

    def __len__(self):
        return len(self.__keymap)

    def __contains__(self, k):
        return k in self.__keymap or k in self.__valmap

    def __getattr__(self, k):
        if k in self:
            return self[k]
        return super(MutableMapping, self).__getattr__(k)

    def items(self):
        return self.__keymap.items()

    def keys(self):
        return self.__keymap.keys()

    def values(self):
        return self.__keymap.values()

    def update(self, *args, **kwargs):
        dd = dict(*args, **kwargs)
        self.__keymap.update(dd)
        self.__valmap = {v: k for k, v in self.__keymap.iteritems()}

