# -*- coding: utf-8 -*-
"""
string normalizer handlers base module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.utilities.string.normalizer.interface import AbstractStringNormalizerBase
from pyrin.utilities.string.normalizer.handlers.exceptions import \
    InvalidStringNormalizerNameError, InvalidStringNormalizerPriorityError


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

        :returns: normalized value.
        :rtype: str
        """

        if value in (None, ''):
            return ''

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
