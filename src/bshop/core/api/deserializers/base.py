# -*- coding: utf-8 -*-
"""
Base deserializer module.
"""

from bshop.core.context import ObjectBase
from bshop.core.exceptions import CoreNotImplementedError


class DeserializerBase(ObjectBase):
    """
    Base deserializer.
    """

    def __init__(self, **options):
        ObjectBase.__init__(self)

    def deserialize(self, value, **options):
        """
        Deserializes the given value.

        :param str value: value to be deserialized.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: deserialized value.
        """

        raise CoreNotImplementedError()
