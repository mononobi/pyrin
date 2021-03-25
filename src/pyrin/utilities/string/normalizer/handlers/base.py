# -*- coding: utf-8 -*-
"""
string normalizer handlers base module.
"""

import re

from abc import abstractmethod
from collections import OrderedDict

import pyrin.utils.dictionary as dict_utils

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utilities.string.normalizer.interface import AbstractStringNormalizerBase
from pyrin.utilities.string.normalizer.handlers.exceptions import FilterMapMustBeDictError, \
    InvalidStringNormalizerNameError, InvalidStringNormalizerPriorityError, \
    FiltersMustBeListError


class StringNormalizerBase(AbstractStringNormalizerBase):
    """
    string normalizer base class.
    """

    def __init__(self, name, priority, *args, **options):
        """
        initializes an instance of StringNormalizerBase.

        :param str name: name of this normalizer.
                         the normalizer will be registered by this name
                         into available normalizers. it must be unique.

        :param int priority: priority of this normalizer.
                             normalizers with higher priority will be executed sooner.

        :raises InvalidStringNormalizerNameError: invalid string normalizer name error.
        :raises InvalidStringNormalizerPriorityError: invalid string normalizer priority error.
        """

        super().__init__()

        if name in (None, '') or name.isspace():
            raise InvalidStringNormalizerNameError('String normalizer name must be '
                                                   'provided for [{normalizer}].'
                                                   .format(normalizer=self))

        if not isinstance(priority, int):
            raise InvalidStringNormalizerPriorityError('String normalizer [{normalizer}] '
                                                       'priority must be an integer.'
                                                       .format(normalizer=name))

        self._set_name(name)
        self._priority = priority

    def normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :keyword bool strip: strip spaces from both ends of value.
                             defaults to True if not provided.

        :keyword bool normalize_none: specifies that if given value is None,
                                      return empty string instead of None.
                                      defaults to False if not provided.

        :returns: normalized value.
        :rtype: str
        """

        normalize_none = options.get('normalize_none', False)
        if value is None and normalize_none is True:
            value = ''

        if value in (None, ''):
            return value

        value = self._normalize(value, **options)
        strip = options.get('strip', True)
        if strip is not False:
            value = value.strip()

        return value

    @abstractmethod
    def _normalize(self, value, **options):
        """
        normalizes the given value.

        this method is intended to be overridden by subclasses.

        :param str value: value to be normalized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: normalized value.
        :rtype: str
        """

        raise CoreNotImplementedError()

    @property
    def priority(self):
        """
        gets the priority of this normalizer.

        :rtype: int
        """

        return self._priority


class FilterNormalizerBase(StringNormalizerBase):
    """
    filter normalizer base class.

    this normalizer will filter provided values from string.
    """

    def __init__(self, name, priority, **options):
        """
        initializes an instance of FilterNormalizerBase.

        :param str name: name of this normalizer.
                         the normalizer will be registered by this name
                         into available normalizers. it must be unique.

        :param int priority: priority of this normalizer.
                             normalizers with higher priority will be executed sooner.

        :keyword list[str] filters: values to be removed from string.

        :keyword dict filter_map: a dict of keys and values to be used
                                  for replacement.

        :note filters, filter_map: the `filters` value have precedence
                                   over `filter_map` value if they have
                                   common keys.

        :raises InvalidStringNormalizerNameError: invalid string normalizer name error.
        :raises InvalidStringNormalizerPriorityError: invalid string normalizer priority error.
        :raises FiltersMustBeListError: filters must be list error.
        :raises FilterMapMustBeDictError: filter map must be dict error.
        """

        super().__init__(name, priority, **options)

        filters = options.get('filters')
        filter_map = options.get('filter_map')

        if filters is not None and not isinstance(filters, list):
            raise FiltersMustBeListError('The provided value for "filters" must be a list.')

        if filter_map is not None and not isinstance(filter_map, dict):
            raise FilterMapMustBeDictError('The provided value for "filter_map" must be a dict.')

        self._filter_map = self._join(filters, filter_map)

    def _join(self, filters, filter_map):
        """
        joins given `filters` and `filter_map` into a single ordered dict.

        the keys will be sorted by length.

        :param list[str] filters: values to be removed from string.

        :param dict filter_map: a dict of keys and values to be used
                                for replacement.

        :note filters, filter_map: the `filters` value have precedence
                                   over `filter_map` value if they have
                                   common keys.

        :rtype: OrderedDict
        """

        if filters is None and filter_map is None:
            return OrderedDict()

        result = dict()
        if filters is not None:
            filters = set(filters)
            for item in filters:
                result[item] = ''

        if filter_map is not None:
            filter_map.update(result)
            result = filter_map

        result = dict_utils.sort_by_key_length(result, reverse=True)
        return result

    def _combine_with_current(self, filters, filter_map):
        """
        combines given inputs with current `filter_maps` and returns a new dict.

        :param list[str] filters: values to be removed from string.

        :param dict filter_map: a dict of keys and values to be used
                                for replacement.

        :note filters, filter_map: the `filters` value have precedence
                                   over `filter_map` value if they have
                                   common keys.

        :rtype: OrderedDict
        """

        if filter_map is None:
            filter_map = dict()

        current = dict(self._filter_map)
        current.update(filter_map)
        filter_map = current
        return self._join(filters, filter_map)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :keyword list[str] filters: values to be removed from string.
                                    this value will be combined with
                                    `self._filter_map` if provided.

        :keyword dict filter_map: a dict of keys and values to be used
                                  for replacement. this value will be
                                  combined with `self._filter_map` if
                                  provided.

        :note filters, filter_map: the `filters` value have precedence
                                   over `filter_map` value if they have
                                   common keys.

        :keyword bool ignore_case: filter matches in case-insensitive way.
                                   defaults to True if not provided.

        :returns: normalized value.
        :rtype: str
        """

        flags = re.IGNORECASE
        ignore_case = options.get('ignore_case', True)
        if ignore_case is False:
            flags = 0

        filter_map = self._combine_with_current(options.get('filters'),
                                                options.get('filter_map'))
        for key, item in filter_map.items():
            value = re.sub(key, item, value, flags=flags)

        return value


class ReplaceNormalizerBase(StringNormalizerBase):
    """
    replace normalizer class.

    this normalizer replaces or removes provided values from string.
    """

    def __init__(self, name, priority, replace_map, **options):
        """
        initializes an instance of ReplaceNormalizerBase.

        :param str name: name of this normalizer.
                         the normalizer will be registered by this name
                         into available normalizers. it must be unique.

        :param int priority: priority of this normalizer.
                             normalizers with higher priority will be executed sooner.

        :param dict replace_map: a dict of keys and values to
                                 be used for replacement or removal.
                                 note that keys must be single length characters.
                                 to remove a key from string, set the key with None
                                 value in the `replace_map`.

        :raises InvalidStringNormalizerNameError: invalid string normalizer name error.
        :raises InvalidStringNormalizerPriorityError: invalid string normalizer priority error.
        """

        super().__init__(name, priority, **options)

        self._map = replace_map
        self._translation_table = str.maketrans(replace_map)

    def _normalize(self, value, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :returns: normalized value.
        :rtype: str
        """

        return value.translate(self._translation_table)
