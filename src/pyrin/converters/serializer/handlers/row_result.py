# -*- coding: utf-8 -*-
"""
serializer handlers row_result module.
"""

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.converters.serializer.handlers.exceptions import ColumnNotExistedError
from pyrin.core.globals import ROW_RESULT
from pyrin.core.structs import DTO


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
                                    available in result, an error will
                                    be raised.

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

        :raises ColumnNotExistedError: column not existed error.

        :rtype: dict
        """

        if len(value) <= 0:
            return DTO()

        requested_columns, rename, excluded_columns = self._extract_conditions(**options)
        base_columns = value.keys()

        if len(requested_columns) <= 0 and len(rename) <= 0 and \
                len(excluded_columns) <= 0:

            return DTO(zip(base_columns, value))

        if len(requested_columns) > 0:
            difference = set(requested_columns).difference(set(base_columns))
            if len(difference) > 0:
                raise ColumnNotExistedError('Requested columns {columns} '
                                            'are not available in result.'
                                            .format(columns=list(difference)))
        else:
            requested_columns = base_columns

        result = DTO()
        for col in requested_columns:
            if col not in excluded_columns:
                result[rename.get(col, col)] = getattr(value, col)

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
                                    available in result, an error will
                                    be raised.

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
