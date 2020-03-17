# -*- coding: utf-8 -*-
"""
serializer row_result module.
"""

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.core.globals import ROW_RESULT
from pyrin.utils.sqlalchemy import row_result_to_dict


@serializer()
class RowResultSerializer(SerializerBase):
    """
    row result serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param ROW_RESULT value: row result value to be serialized.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, all columns will be returned.
                                    note that the columns must be a subset of all
                                    columns of this `ROW_RESULT`, otherwise
                                    it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: dict
        """

        return row_result_to_dict(value, **options)

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: ROW_RESULT
        """

        return ROW_RESULT
