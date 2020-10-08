# -*- coding: utf-8 -*-
"""
serializer handlers list module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.api.schema.result import ResultSchema
from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase


@serializer()
class ListSerializer(SerializerBase):
    """
    list serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        returns serialized list on success or `NULL` object if serialization fails.

        :param list[object] value: list value to be serialized.

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result.

        :keyword int start_index: the initial value of row index.

        :returns: serialized list of objects
        :rtype: list[dict]
        """

        if len(value) <= 0:
            return []

        indexed = options.get('indexed', False)
        index_name = options.get('index_name', ResultSchema.DEFAULT_INDEX_NAME)
        start_index = options.get('start_index', ResultSchema.DEFAULT_START_INDEX)
        result = []

        # if indexing is requested, all items must be a dict after serialization.
        # so we just check the first item to be a dict after serialization, otherwise
        # no indexing will be done.
        first_item = serializer_services.serialize(value[0], **options)
        if indexed is False or not isinstance(first_item, dict):
            indexed = False

        if indexed is True:
            first_item[index_name] = start_index
            start_index = start_index + 1

        result.append(first_item)
        value = value[1:]

        # we set 'indexed=False' to prevent inner lists from indexing.
        options.update(indexed=False)
        for item in value:
            converted = serializer_services.serialize(item, **options)
            if indexed is True:
                converted[index_name] = start_index
                start_index = start_index + 1

            result.append(converted)

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: type[list]
        """

        return list
