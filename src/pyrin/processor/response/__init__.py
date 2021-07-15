# -*- coding: utf-8 -*-
"""
response package.
"""

from pyrin.packaging.base import Package


class ResponsePackage(Package):
    """
    response package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    CONFIG_STORE_NAMES = ['response']
    COMPONENT_NAME = 'processor.response.component'
