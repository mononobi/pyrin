# -*- coding: utf-8 -*-
"""
caching local containers dict module.
"""

from pyrin.caching.local.containers.base import LocalCacheContainerBase
from pyrin.core.compat import PythonOrderedDict


class OrderedDictContainer(PythonOrderedDict, LocalCacheContainerBase):
    """
    ordered dict container class.

    it is actually a regular ordered dict.
    it is inherited from `OrderedDict` instead of `dict` to let efficiently
    remove items in `FIFO` or `LIFO` order when items count limit is reached.

    note that as OrderedDict implementation is in C, we could not subclass
    it normally. so we have to use the python implementation of OrderedDict.
    """

    def set(self, key, value, *args, **kwargs):
        """
        sets a new value into cached items.

        :param object key: hashable key of the cache to be registered.
        :param object value: value to be cached.
        """

        self[key] = value

    def slice(self, count, last=False):
        """
        gets a slice of items of this container with the count length.

        :param int count: number of items to include in slice.

        :param bool last: specifies that slice must include items from end.
                          defaults to False if not provided.

        :returns: iterable
        """

        items = list(self.keys())
        if last is not True:
            return items[:count]
        else:
            return items[count * -1:]
