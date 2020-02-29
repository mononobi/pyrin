# -*- coding: utf-8 -*-
"""
deserializer package.
"""

from pyrin.packaging.base import Package


class DeserializerPackage(Package):
    """
    deserializer package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'converters.deserializer.component'
