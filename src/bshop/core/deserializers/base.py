# -*- coding: utf-8 -*-
"""
Base deserializer module.
"""

from bshop.core.context import ObjectBase


class DeserializerBase(ObjectBase):
    """
    Base deserializer.
    """

    def __init__(self, **options):
        super(DeserializerBase, self).__init__()

    def deserialize(self, value):
        """
        Deserializes the given value.

        :param str value: value to be deserialized.

        :return: deserialized value.

        :raises: :class:`NotImplementedError`: not implemented error.
        """

        raise NotImplementedError()
