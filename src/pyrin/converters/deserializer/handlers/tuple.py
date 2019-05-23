# -*- coding: utf-8 -*-
"""
deserializer tuple module.
"""

import re

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.handlers.base import DeserializerBase, \
    StringCollectionDeserializerBase
from pyrin.converters.deserializer.decorators import deserializer


@deserializer()
class TupleDeserializer(DeserializerBase):
    """
    tuple deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of TupleDeserializer.
        """

        DeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes every possible value available in input tuple.
        and gets a new deserialized tuple.

        :param tuple value: value that should be deserialized.

        :rtype: tuple
        """

        if not self.is_deserializable(value, **options):
            return None

        result_list = [item for item in value]

        index = 0
        for item in result_list:
            deserialized_value = None

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item)

            if deserialized_value is not None:
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
class StringTupleDeserializer(StringCollectionDeserializerBase):
    """
    string tuple deserializer class.
    note that this deserializer could only handle tuples with single depth.
    meaning that nested tuples are not supported. and also nested lists or
    dictionaries or sets or any other collections are not supported and
    stops deserialization.
    for example: (1, (2, 4), [5, 4]) will not be deserialized.
    """

    # matches the tuple inside string.
    # example: (), (1), (1,), (1,2),(1,2,)
    # all of these values will be matched.
    TUPLE_REGEX = re.compile(r'^\(\)$|^\(.+(,.+)*\)$')

    def __init__(self, **options):
        """
        creates an instance of StringTupleDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted patterns
                                                             and their length for tuple
                                                             deserialization.

        :type accepted_formats: list[tuple(Pattern format, int length)]

        :keyword list[str] invalid_chars: custom invalid characters that make deserialization
                                          impossible for this deserializer.
        """

        StringCollectionDeserializerBase.__init__(self, **options)

    def deserialize(self, value, **options):
        """
        deserializes the given value.
        returns None if deserialization fails.

        :param str value: value to be deserialized.

        :rtype: tuple
        """

        deserializable, pattern = self.is_deserializable(value, **options)
        if not deserializable:
            return None

        value = value.strip()

        # removing the first '(' and last ')' from value.
        value = value[1:-1]
        items = value.split(',')
        temp_list = []
        for item in items:
            if len(item.strip()) > 0:
                temp_list.append(item)

        # this deserializer does not handle nested tuples, so it won't
        # check whether each item is deserializable or not.
        return deserializer_services.deserialize(tuple(temp_list))

    def get_default_formats(self):
        """
        gets default accepted patterns that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.TUPLE_REGEX, self.UNDEF_LENGTH)]

    def get_default_invalid_chars(self):
        """
        returns a list of default invalid characters which make
        deserialization impossible for this deserializer.

        :rtype: list[str]
        """

        return ['[', ']', '{', '}']
