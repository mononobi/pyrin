# -*- coding: utf-8 -*-
"""
schema result module.
"""

import pyrin.database.model.services as model_services

from pyrin.converters.serializer.base import SerializerBase
from pyrin.converters.serializer.entity import CoreEntitySerializer
from pyrin.converters.serializer.keyed_tuple import CoreKeyedTupleSerializer
from pyrin.core.context import CoreObject, DTO
from pyrin.core.globals import LIST_TYPES
from pyrin.api.schema.exceptions import SchemaColumnsOrReplaceIsRequiredError, \
    ObjectIsNotSerializableError, InvalidSerializerTypeError, ColumnNotExistedError, \
    InvalidReplaceKeysError


class ResultSchema(CoreObject):
    """
    result schema class.
    """

    def __init__(self, columns=None, replace=None, **options):
        """
        initializes an instance of ResultSchema.

        note that at least one of `columns` or `replace` must be provided.

        :param list[str] columns: column names to be included in result.

        :param dict replace: a dict containing original column names as
                             keys, and column names that must be exposed
                             instead of original names, as values.
                             for example if `replace = dict(real_name='new_name')`
                             then, the value of `real_name` column in result will
                             be returned as `new_name` column.
                             note that if you provide `columns` input too, then the
                             keys of replace dict must be a subset of `columns`.

        :keyword SerializerBase entity_serializer: serializer instance to be used
                                                   for entities. defaults to
                                                   `CoreEntitySerializer` if
                                                   not provided.

        :keyword SerializerBase keyed_tuple_serializer: serializer instance to be used
                                                        for keyed tuples. defaults to
                                                        `CoreKeyedTupleSerializer` if
                                                        not provided.

        :raises SchemaColumnsOrReplaceIsRequiredError: schema columns or replace
                                                       is required error.

        :raises InvalidReplaceKeysError: invalid replace keys error.
        :raises InvalidSerializerTypeError: invalid serializer type error.
        """

        super().__init__()

        if (columns is None or len(columns) <= 0) and \
                (replace is None or len(replace) <= 0):
            raise SchemaColumnsOrReplaceIsRequiredError('Result schema "columns" or '
                                                        '"replace" must be provided.')

        if columns is None:
            columns = []

        if replace is None:
            replace = {}

        if len(columns) > 0 and len(replace) > 0:
            difference = set(replace.keys()).difference(set(columns))
            if len(difference) > 0:
                raise InvalidReplaceKeysError('"replace" keys {replace} are not present '
                                              'in "columns". when providing both "columns" '
                                              'and "replace" inputs, "replace" keys must '
                                              'be a subset of "columns".'
                                              .format(replace=list(difference)))

        self._columns = columns
        self._replace = replace

        entity_serializer = options.get('entity_serializer', None)
        keyed_tuple_serializer = options.get('keyed_tuple_serializer', None)

        if entity_serializer is None:
            entity_serializer = CoreEntitySerializer()

        if keyed_tuple_serializer is None:
            keyed_tuple_serializer = CoreKeyedTupleSerializer()

        message = 'Input parameter [{instance}] is not an instance of [{base}].'
        if not isinstance(entity_serializer, SerializerBase):
            raise InvalidSerializerTypeError(message.format(instance=entity_serializer,
                                                            base=SerializerBase))

        if not isinstance(keyed_tuple_serializer, SerializerBase):
            raise InvalidSerializerTypeError(message.format(instance=keyed_tuple_serializer,
                                                            base=SerializerBase))

        self._entity_serializer = entity_serializer
        self._keyed_tuple_serializer = keyed_tuple_serializer

    @property
    def columns(self):
        """
        gets the columns attribute of this schema.

        these are the columns that must be returned from the result.

        :rtype: list[str]
        """

        return self._columns

    @property
    def replace(self):
        """
        gets the replace attribute of this schema.

        these are the columns that must be returned
        with modified names from the result.

        :rtype: dict
        """

        return self._replace

    def filter(self, value, **options):
        """
        filters the value based on current schema.

        :param Union[list[CoreEntity],
                     list[AbstractKeyedTuple],
                     CoreEntity,
                     AbstractKeyedTuple] value: value or values to be filtered.

        :raises ColumnNotExistedError: column not existed error.
        :raises ObjectIsNotSerializableError: object is not serializable error.

        :rtype: Union[dict, list[dict]]
        """

        if isinstance(value, LIST_TYPES):
            return self._serialize_list(value)

        return self._serialize(value)

    def _serialize(self, item, **options):
        """
        serializes the given item based on current schema.

        :param Union[CoreEntity, AbstractKeyedTuple] item: item to be serialized.

        :raises ColumnNotExistedError: column not existed error.
        :raises ObjectIsNotSerializableError: object is not serializable error.

        :rtype: dict
        """

        if item is None:
            return DTO()

        options.pop('columns', None)
        result = None
        if model_services.is_core_entity(item):
            result = self._entity_serializer.serialize(item, columns=self.columns,
                                                       **options)
        elif model_services.is_abstract_keyed_tuple(item):
            result = self._keyed_tuple_serializer.serialize(item, columns=self.columns,
                                                            **options)
        else:
            raise ObjectIsNotSerializableError('Object [{instance}] of type '
                                               '[{type_}] is not serializable.'
                                               .format(instance=item, type_=type(item)))

        if self.replace is not None and len(self.replace) > 0 and len(result) > 0:
            difference = set(self.replace.keys()).difference(set(result.keys()))
            if len(difference) > 0:
                raise ColumnNotExistedError('Columns {columns} are not available in result.'
                                            .format(columns=list(difference)))

            for original_column, new_column in self.replace.items():
                value = result.pop(original_column)
                result[new_column] = value

        return result

    def _serialize_list(self, items, **options):
        """
        serializes the given items based on current schema.

        :param Union[list[CoreEntity], list[AbstractKeyedTuple]] items: items to
                                                                        be serialized.

        :raises ColumnNotExistedError: column not existed error.
        :raises ObjectIsNotSerializableError: object is not serializable error.

        :rtype: list[dict]
        """

        if items is None or len(items) <= 0:
            return []

        return [self._serialize(value, **options) for value in items]
