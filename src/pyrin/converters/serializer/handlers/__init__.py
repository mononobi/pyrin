# -*- coding: utf-8 -*-
"""
serializer handlers package.
"""

from pyrin.packaging.base import Package


class SerializerHandlersPackage(Package):
    """
    serializer handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.api']
