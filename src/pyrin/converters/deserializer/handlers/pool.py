# -*- coding: utf-8 -*-
"""
deserializer pool module.
"""

import re

from sqlalchemy.pool import Pool, NullPool, AssertionPool, QueuePool, \
    SingletonThreadPool, StaticPool

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase
from pyrin.core.globals import NULL


@deserializer()
class PoolDeserializer(StringPatternDeserializerBase):
    """
    pool deserializer class.
    """

    # matches the pool class inside string.
    # example: Pool, NullPool, AssertionPool, QueuePool, SingletonThreadPool, StaticPool
    # matching are case-insensitive.
    POOL_REGEX = re.compile(r'^Pool$', re.IGNORECASE)
    NULL_POOL_REGEX = re.compile(r'^NullPool$', re.IGNORECASE)
    ASSERTION_POOL_REGEX = re.compile(r'^AssertionPool$', re.IGNORECASE)
    QUEUE_POOL_REGEX = re.compile(r'^QueuePool$', re.IGNORECASE)
    SINGLETON_THREAD_POOL_REGEX = re.compile(r'^SingletonThreadPool$', re.IGNORECASE)
    STATIC_POOL_REGEX = re.compile(r'^StaticPool$', re.IGNORECASE)

    def __init__(self, **options):
        """
        creates an instance of PoolDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted formats
                                                             and their length for pool
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

        self._converter_map = self._get_converter_map()

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: Pool
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        return self._converter_map[pattern]

    def get_default_formats(self):
        """
        gets default accepted formats that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.POOL_REGEX, 4),
                (self.NULL_POOL_REGEX, 8),
                (self.ASSERTION_POOL_REGEX, 13),
                (self.QUEUE_POOL_REGEX, 9),
                (self.SINGLETON_THREAD_POOL_REGEX, 19),
                (self.STATIC_POOL_REGEX, 10)]

    def _get_converter_map(self):
        """
        gets converter map dictionary.

        :returns: dict(Pattern format: Pool pool)

        :rtype: dict
        """

        return {self.POOL_REGEX: Pool,
                self.NULL_POOL_REGEX: NullPool,
                self.ASSERTION_POOL_REGEX: AssertionPool,
                self.QUEUE_POOL_REGEX: QueuePool,
                self.SINGLETON_THREAD_POOL_REGEX: SingletonThreadPool,
                self.STATIC_POOL_REGEX: StaticPool}
