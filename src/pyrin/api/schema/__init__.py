# -*- coding: utf-8 -*-
"""
schema package.
"""

from pyrin.packaging.base import Package


class SchemaPackage(Package):
    """
    schema package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'api.schema.component'
