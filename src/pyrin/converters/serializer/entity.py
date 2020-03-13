# -*- coding: utf-8 -*-
"""
serializer entity module.
"""

from pyrin.converters.serializer.base import SerializerBase
from pyrin.utils.sqlalchemy import entity_to_dict


class CoreEntitySerializer(SerializerBase):
    """
    core entity serializer class.
    """

    def serialize(self, value, **options):
        """
        serializes the given value.

        :param CoreEntity value: entity value to be serialized.

        :keyword bool exposed_only: if set to False, it returns all
                                    columns of the entity as dict.
                                    if not provided, defaults to True.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, the columns in exposed
                                    columns or all columns will be returned.
                                    note that the columns must be a subset of
                                    all columns or exposed columns of this
                                    entity considering "exposed_only" parameter,
                                    otherwise it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :type: dict
        """

        return entity_to_dict(value, **options)
