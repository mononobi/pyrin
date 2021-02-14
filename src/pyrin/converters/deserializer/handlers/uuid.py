# -*- coding: utf-8 -*-
"""
deserializer handlers uuid module.
"""

import pyrin.utils.unique_id as uuid_utils

from pyrin.core.globals import NULL
from pyrin.utils.unique_id import UUID_REGEX
from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import StringPatternDeserializerBase


@deserializer()
class UUIDDeserializer(StringPatternDeserializerBase):
    """
    uuid deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of UUIDDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  formats and their min and
                                                                  max length for uuid
                                                                  deserialization.

        :note accepted_formats: list[tuple[Pattern format, int min_length, int max_length]]

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.

        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :keyword Pattern matching_pattern: the pattern that has matched the value.

        :rtype: uuid.UUID
        """

        result = uuid_utils.try_get_uuid(value)
        if result is None:
            return NULL

        return result

    @property
    def default_formats(self):
        """
        gets default accepted formats that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(UUID_REGEX, 36, 36)]
