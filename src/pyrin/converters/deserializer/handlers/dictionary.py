# -*- coding: utf-8 -*-
"""
deserializer handlers dictionary module.
"""

import re

import flask.json as flask_json

import pyrin.converters.deserializer.services as deserializer_services

from pyrin.converters.deserializer.decorators import deserializer
from pyrin.core.structs import DTO
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

        :keyword bool internal: specifies that this deserializer is internal.
                                internal deserializers will not be used for
                                deserializing client inputs.
                                defaults to False if not provided.
        """

        super().__init__(**options)

    def _deserialize(self, value, **options):
        """
        deserializes every possible value available in input dictionary.

        gets a new deserialized dictionary, leaving the input unchanged.

        :param dict value: value that should be deserialized.

        :rtype: dict
        """

        result = DTO(**value)
        for key, item in result.items():
            result[key] = deserializer_services.deserialize(item, **options)

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this deserializer.

        which could deserialize values from this type.

        :rtype: type[dict]
        """

        return dict


@deserializer()
class StringDictionaryDeserializer(StringPatternDeserializerBase):
    """
    string dictionary deserializer class.
    """

    # default min for this deserializer is 2 because
    # it should at least have { and } at both ends.
    DEFAULT_MIN = 2

    # matches a dictionary inside string, all of these values will be matched.
    # example: {}, {22: 1}, {'key1': 1, 'key2': 2}
    DICT_REGEX = re.compile(r'^{.*}$')

    def __init__(self, **options):
        """
        creates an instance of StringDictionaryDeserializer.

        :keyword list[tuple[Pattern, int, int]] accepted_formats: a list of custom accepted
                                                                  patterns and their min and
                                                                  max length for dictionary
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

        :rtype: dict
        """

        try:
            dict_value = flask_json.loads(value)
            if dict_value is not None:
                return deserializer_services.deserialize(dict_value, **options)

            return NULL
        except Exception:
            return NULL

    @property
    def default_formats(self):
        """
        gets default accepted patterns that this deserializer could deserialize value from.

        :returns: list[tuple[Pattern format, int min_length, int max_length]]
        :rtype: list[tuple[Pattern, int, int]]
        """

        return [(self.DICT_REGEX, self.UNDEF_LENGTH, self.UNDEF_LENGTH)]
