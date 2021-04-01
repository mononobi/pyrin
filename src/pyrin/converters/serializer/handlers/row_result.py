# -*- coding: utf-8 -*-
"""
serializer handlers row_result module.
"""

import pyrin.api.schema.services as schema_services

from pyrin.core.structs import DTO
from pyrin.core.globals import ROW_RESULT
from pyrin.database.model.base import BaseEntity
from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase


@serializer()
class RowResultSerializer(SerializerBase):
    """
    row result serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param ROW_RESULT value: row result value to be serialized.

        :keyword list[str] columns: column names to be included in result.
                                    for example:
                                    `columns=['id', 'name', 'age']`
                                    if provided column names are not
                                    available in result, they will be ignored.

        :keyword dict[str, str] rename: column names that must be renamed in the result.
                                        it must be a dict with keys as original column
                                        names and values as new column names that should
                                        be exposed instead of original column names.
                                        for example:
                                        `rename=dict(age='new_age', name='new_name')`
                                        if provided rename columns are not available in
                                        result, they will be ignored.

        :keyword list[str] exclude: column names to be excluded from
                                    result. for example:
                                    `exclude=['id', 'name', 'age']`
                                    if provided excluded columns are not
                                    available in result, they will be
                                    ignored.

        :keyword ResultSchema result_schema: result schema instance to be
                                             used to create computed columns.
                                             defaults to None if not provided.

        :rtype: dict
        """

        if len(value) <= 0:
            return DTO()

        requested_columns, rename, excluded_columns = self._extract_conditions(**options)
        base_columns = list(value._mapping.keys())
        entities = DTO()
        to_remove_keys = []
        for key, instance in value._mapping.items():
            if isinstance(instance, BaseEntity):
                computed_entity_columns = schema_services.get_computed_entity_columns(instance,
                                                                                      **options)
                serialized_entity = instance.to_dict(**options)
                serialized_entity.update(computed_entity_columns)
                entities[key] = serialized_entity
                to_remove_keys.append(key)
                excluded_columns.append(key)

        computed_row_columns = schema_services.get_computed_row_columns(value, **options)

        if len(requested_columns) <= 0 and \
                len(rename) <= 0 and len(excluded_columns) <= 0:

            result = DTO(value._mapping)
            result.update(computed_row_columns)
            return result

        for item in to_remove_keys:
            base_columns.remove(item)

        if len(requested_columns) > 0:
            requested_columns = set(requested_columns).intersection(set(base_columns))
        else:
            requested_columns = base_columns

        result = DTO()
        for key, entity in entities.items():
            result.update(entity)

        for col in requested_columns:
            if col not in excluded_columns:
                result[rename.get(col, col)] = value._mapping.get(col)

        result.update(computed_row_columns)
        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: type[ROW_RESULT]
        """

        return ROW_RESULT

    def _extract_conditions(self, **options):
        """
        extracts all conditions available in given options.

        it extracts columns, rename and exclude values.

        :keyword list[str] columns: column names to be included in result.
                                    for example:
                                    `columns=['id', 'name', 'age']`
                                    if provided column names are not
                                    available in result, they will be ignored.

        :keyword dict[str, str] rename: column names that must be renamed in the result.
                                        it must be a dict with keys as original column
                                        names and values as new column names that should
                                        be exposed instead of original column names.
                                        for example:
                                        `rename=dict(age='new_age', name='new_name')`
                                        if provided rename columns are not available in
                                        result, they will be ignored.

        :keyword list[str] exclude: column names to be excluded from
                                    result. for example:
                                    `exclude=['id', 'name', 'age']`
                                    if provided excluded columns are not
                                    available in result, they will be
                                    ignored.

        :returns: tuple[list[str column_name],
                        dict[str original_column, str new_column],
                        list[str excluded_column]]

        :rtype: tuple[list[str], dict[str, str], list[str]]
        """

        columns = options.get('columns', None)
        rename = options.get('rename', None)
        exclude = options.get('exclude', None)

        if columns is None:
            columns = []

        if rename is None:
            rename = {}

        if exclude is None:
            exclude = []

        return columns, rename, exclude
