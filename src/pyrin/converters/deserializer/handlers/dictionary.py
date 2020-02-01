# -*- coding: utf-8 -*-
"""
deserializer dictionary module.
"""

import re

import flask.json as flask_json

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.core.context import DTO
from pyrin.core.globals import NULL
from pyrin.converters.deserializer.handlers.base import DeserializerBase, \
    StringPatternDeserializerBase


@deserializer()
class DictionaryDeserializer(DeserializerBase):
    """
    dictionary deserializer class.
    """

    def __init__(self, **options):
        """
        creates an instance of DictionaryDeserializer.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes every possible value available in input dictionary.
        and gets a new deserialized dictionary, leaving the input unchanged.

        :param dict value: value that should be deserialized.

        :rtype: dict
        """

        if not self.is_deserializable(value, **options):
            return NULL

        result = DTO(**value)

        for key in result.keys():
            item = result.get(key)
            deserialized_value = NULL

            if self.is_deserializable(item, **options):
                deserialized_value = self.deserialize(item)
            else:
                deserialized_value = deserializer_services.deserialize(item, **options)

            if deserialized_value is not NULL:
                result[key] = deserialized_value
            continue

        return result

    def get_accepted_type(self):
        """
        gets the accepted type for this deserializer
        which could deserialize values from this type.

        :rtype: type
        """

        return dict


@deserializer()
class StringDictionaryDeserializer(StringPatternDeserializerBase):
    """
    string dictionary deserializer class.
    """

    # default min for this deserializer is 2 because
    # it should at least has { and } at both ends.
    DEFAULT_MIN = 2

    # matches a dictionary inside string, all of these values will be matched.
    # example: {}, {22: 1}, {'key1': 1, 'key2': 2}
    DICT_REGEX = re.compile(r'^{.*}$')

    def __init__(self, **options):
        """
        creates an instance of StringDictionaryDeserializer.

        :keyword list[tuple(Pattern, int)] accepted_formats: a list of custom accepted patterns
                                                             and their length for dictionary
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

        try:
            dict_value = flask_json.loads(value)
            if dict_value is not None:
                deserialized_value = deserializer_services.deserialize(dict_value, **options)
                return deserialized_value

            return NULL
        except Exception:
            return NULL

    def get_default_formats(self):
        """
        gets default accepted patterns that this
        deserializer could deserialize value from.

        :return: list(tuple(Pattern format, int length))

        :rtype: list(tuple(Pattern, int))
        """

        return [(self.DICT_REGEX, self.UNDEF_LENGTH)]
