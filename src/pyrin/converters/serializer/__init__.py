# -*- coding: utf-8 -*-
"""
serializer package.
"""

from pyrin.packaging.base import Package


class SerializerPackage(Package):
    """
    serializer package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'converters.serializer.component'
