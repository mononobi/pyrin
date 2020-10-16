# -*- coding: utf-8 -*-
"""
string normalizer interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class StringNormalizerSingletonMeta(MultiSingletonMeta):
    """
    string normalizer singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractStringNormalizerBase(CoreObject, metaclass=StringNormalizerSingletonMeta):
    """
    abstract string normalizer base class.
    """

    @abstractmethod
    def normalize(self, value, *args, **options):
        """
        normalizes the given value.

        :param str value: value to be normalized.

        :keyword bool strip: strip spaces from both ends of value.
                             defaults to True if not provided.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: normalized value.
        :rtype: str
        """

        raise CoreNotImplementedError()
