# -*- coding: utf-8 -*-
"""
deserializer handlers pool module.
"""

import re

from sqlalchemy.pool import Pool, NullPool, AssertionPool, QueuePool, \
    SingletonThreadPool, StaticPool

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase


@deserializer()
class PoolDeserializer(StringPatternDeserializerBase):
    """
    pool deserializer class.
    """

    # matches the pool class inside string.
    # example: Pool, NullPool, AssertionPool, QueuePool, SingletonThreadPool, StaticPool
    # matching is case-insensitive.
    POOL_REGEX = re.compile(r'^Pool$', re.IGNORECASE)
    NULL_POOL_REGEX = re.compile(r'^NullPool$', re.IGNORECASE)
    ASSERTION_POOL_REGEX = re.compile(r'^AssertionPool$', re.IGNORECASE)
    QUEUE_POOL_REGEX = re.compile(r'^QueuePool$', re.IGNORECASE)
    SINGLETON_THREAD_POOL_REGEX = re.compile(r'^SingletonThreadPool$', re.IGNORECASE)
    STATIC_POOL_REGEX = re.compile(r'^StaticPool$', re.IGNORECASE)

    def __init__(self, **options):
        """
        creates an instance of PoolDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for pool
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]
        """

        options.update(internal=True)
        super().__init__(**options)

        self._converter_map = self._get_converter_map()

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: type[Pool]
        """

        pattern = options.pop('matching_pattern')
        return self._converter_map[pattern]

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.POOL_REGEX, 4, 4),
                (self.NULL_POOL_REGEX, 8, 8),
                (self.ASSERTION_POOL_REGEX, 13, 13),
                (self.QUEUE_POOL_REGEX, 9, 9),
                (self.SINGLETON_THREAD_POOL_REGEX, 19, 19),
                (self.STATIC_POOL_REGEX, 10, 10)]

    def _get_converter_map(self):
        """
        gets converter map dictionary.

        :returns: dict[Pattern format: type pool]
        :rtype: dict
        """

        return {self.POOL_REGEX: Pool,
                self.NULL_POOL_REGEX: NullPool,
                self.ASSERTION_POOL_REGEX: AssertionPool,
                self.QUEUE_POOL_REGEX: QueuePool,
                self.SINGLETON_THREAD_POOL_REGEX: SingletonThreadPool,
                self.STATIC_POOL_REGEX: StaticPool}
