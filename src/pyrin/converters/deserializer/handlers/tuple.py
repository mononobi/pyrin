# -*- coding: utf-8 -*-
"""
deserializer tuple module.
"""

import re

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.converters.deserializer.handlers.base import DeserializerBase, \
    StringPatternDeserializerBase
from pyrin.core.globals import NULL


@deserializer()
class TupleDeserializer(DeserializerBase):
    """
    tuple deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of TupleDeserializer.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes every possible value available in input tuple.
        and gets a new deserialized tuple.

        :param tuple value: value that should be deserialized.

        :rtype: tuple
        """

        if not self.is_deserializable(value, **options):
            return NULL

        result_list = [item for item in value]

        index = 0
        for item in result_list:
            deserialized_value = NULL

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item, **options)

            if deserialized_value is not NULL:
                result_list[index] = deserialized_value

            index += 1
            continue

        return tuple(result_list)

    def get_accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return tuple


@deserializer()
class StringTupleDeserializer(StringPatternDeserializerBase):
    """
    string tuple deserializer class.
    note that this deserializer could only handle tuples with single depth.
    meaning that nested tuples are not supported. and also nested lists or
    dictionaries or sets or any other collections are not supported and
    stops deserialization.
    for example: (1, (2, 4), [5, 4]) will not be deserialized.
    """

    # default min for this deserializer is 2 because
    # it should at least has ( and ) at both ends.
    DEFAULT_MIN = 2

    # matches a tuple inside string, all of these values will be matched.
    # example: (), (1), (1,), (1,2), (1,2,)
    # it won't accept nested collections, all of these values won't match.
    # example: ([]), (1, {2: 4}, (2,3))
    TUPLE_REGEX = re.compile(r'^\(\)$|^\([^\(\){}\[\]]+(,[^\(\){}\[\]]+)*\)$')

    def __init__(self, **options):
        """
        creates an instance of StringTupleDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted patterns
                                                             and their length for tuple
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes the given value.
        returns `NULL` object if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: tuple
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return NULL

        value = value.strip()

        # removing the first '(' and last ')' from value.
        value = value[1:-1]
        items = value.split(',')
        temp_list = []
        for item in items:
            if len(item.strip()) > 0:
                temp_list.append(item.strip())

        # this deserializer does not handle nested tuples, so it won't
        # check whether each item is deserializable or not.
        return deserializer_services.deserialize(tuple(temp_list), **options)

    def get_default_formats(self):
        """
        gets default accepted patterns that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.TUPLE_REGEX, self.UNDEF_LENGTH)]
