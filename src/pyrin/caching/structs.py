# -*- coding: utf-8 -*-
"""
caching structs module.
"""

from collections import OrderedDict

from pyrin.core.globals import LIST_TYPES
from pyrin.caching.globals import NOT_HASHABLE_TYPES


class CacheableDict(OrderedDict):
    """
    cacheable dict class.

    this class is a normal ordered dict but it is hashable and could
    be used as dict key.
    """

    def __init__(self, mapping=None, **kwargs):
        """
        initializes an instance of CacheableDict.

        :param dict | CacheableDict | iterable mapping: values to create a dict form them.
        """

        cacheable_kwargs = {}
        if len(kwargs) > 0:
            cacheable_kwargs = self._convert_dict(kwargs)

        if isinstance(mapping, CacheableDict):
            super().__init__(self._sort_list(self._union_lists(mapping.items(),
                                                               cacheable_kwargs.items())))
        elif isinstance(mapping, dict):
            temp = {}
            for key, value in mapping.items():
                if isinstance(value, NOT_HASHABLE_TYPES):
                    temp[key] = self._convert(value)
                else:
                    temp[key] = value

            super().__init__(self._sort_list(self._union_lists(temp.items(),
                                                               cacheable_kwargs.items())))

        elif isinstance(mapping, LIST_TYPES):
            temp = []
            for key, value in mapping:
                if isinstance(value, NOT_HASHABLE_TYPES):
                    temp.append((key, self._convert(value)))
                else:
                    temp.append((key, value))

            super().__init__(self._sort_list(self._union_lists(temp,
                                                               cacheable_kwargs.items())))

        else:
            super().__init__(self._sort_list(cacheable_kwargs.items()))

    def __hash__(self):
        """
        gets the hash of current dict.

        :rtype: int
        """

        return hash(tuple(self.items()))

    def __eq__(self, other):
        """
        implements the equality operator.

        :param object other: other instance to check for equality.

        :rtype: bool
        """

        if not isinstance(other, CacheableDict):
            return False

        self_len = len(self)
        other_len = len(other)
        if self_len != other_len:
            return False

        if self_len == 0:
            return True

        return hash(self) == hash(other)

    def __ne__(self, other):
        """
        implements the not equality operator.

        :param object other: other instance to check for not equality.

        :rtype: bool
        """

        return not self == other

    def _union_lists(self, first, second):
        """
        gets the union of two iterables.

        :param iterable first: first iterable.
        :param iterable second: second iterable.

        :rtype: list
        """

        first = list(first)
        second = list(second)
        first.extend(second)
        return first

    def _convert(self, value):
        """
        converts all required values of given object to be hashable.

        if given object is not a dict or collection it returns the same input value.

        :param dict | list | tuple | set value: a dict or collection.

        :rtype: CacheableDict | tuple | object
        """

        if isinstance(value, dict):
            return self._convert_dict(value)
        elif isinstance(value, LIST_TYPES):
            return self._convert_list(value)
        return value

    def _convert_dict(self, value):
        """
        converts all required values of given dict to be hashable.

        :param dict value: dict to convert its value.

        :rtype: CacheableDict
        """

        return CacheableDict(value)

    def _convert_list(self, items):
        """
        converts all required values of different items of given iterable.

        :param list | tuple | set items: items to convert their values.

        :rtype: tuple
        """

        results = []
        for item in items:
            results.append(self._convert(item))

        return tuple(self._sort_list(results))

    def _sort_list(self, value):
        """
        returns the sorted list.

        if values are not comparable, it returns an unsorted list.

        :param iterable value: value ot be sorted.

        :rtype: list
        """

        try:
            # try to sort by value if all values are same type.
            return sorted(value)
        except TypeError:
            # fallback to unsorted values when value types are incomparable.
            return list(value)
