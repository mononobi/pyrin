# -*- coding: utf-8 -*-
"""
serializer row_result module.
"""

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
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
                                    available in result, they will be
                                    ignored.

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

        :rtype: dict
        """

        if len(value) <= 0:
            return DTO()

        columns = options.get('columns', None)
        original_result = DTO(zip(value.keys(), value))
        if columns is None or len(columns) <= 0:
            return original_result

        result = DTO()
        for col in columns:
            result[col] = original_result[col]

        return result

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: ROW_RESULT
        """

        return ROW_RESULT
