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

    @classmethod
    def serialize(cls, value, **options):
        """
        serializes the given value.

        :param CoreEntity value: entity value to be serialized.

        :keyword bool exposed_only: if set to False, it returns all
                                    columns of the entity as dict.
                                    if not provided, defaults to True.

        :type: dict
        """

        exposed = options.get('exposed_only', True)
        return entity_to_dict(value, exposed_only=exposed)
