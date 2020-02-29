# -*- coding: utf-8 -*-
"""
configuration package.
"""

from pyrin.packaging.base import Package


class ConfigurationPackage(Package):
    """
    configuration package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.converters.deserializer']
    COMPONENT_NAME = 'configuration.component'
