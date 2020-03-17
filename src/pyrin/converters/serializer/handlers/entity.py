# -*- coding: utf-8 -*-
"""
serializer entity module.
"""

from pyrin.converters.serializer.decorators import serializer
from pyrin.converters.serializer.handlers.base import SerializerBase
from pyrin.database.model.base import BaseEntity
from pyrin.utils.sqlalchemy import entity_to_dict


@serializer()
class BaseEntitySerializer(SerializerBase):
    """
    base entity serializer class.
    """

    def _serialize(self, value, **options):
        """
        serializes the given value.

        :param BaseEntity value: entity value to be serialized.

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

        :rtype: dict
        """

        return entity_to_dict(value, **options)

    @property
    def accepted_type(self):
        """
        gets the accepted type for this serializer.

        which could serialize values from this type.

        :rtype: BaseEntity
        """

        return BaseEntity
