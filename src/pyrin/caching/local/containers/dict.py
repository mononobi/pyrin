# -*- coding: utf-8 -*-
"""
caching local containers dict module.
"""

from collections import OrderedDict

from pyrin.caching.local.containers.base import LocalCacheContainerBase


class OrderedDictContainer(OrderedDict, LocalCacheContainerBase):
    """
    ordered dict container class.

    it is actually a regular ordered dict.
    it is inherited from `OrderedDict` instead of `dict` to let efficiently
    remove items in `FIFO` or `LIFO` order when items count limit is reached.
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
