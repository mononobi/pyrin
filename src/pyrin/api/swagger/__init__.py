# -*- coding: utf-8 -*-
"""
swagger package.
"""

from pyrin.packaging.base import Package


class SwaggerPackage(Package):
    """
    swagger package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.globalization.locale',
               'pyrin.globalization.datetime']

    COMPONENT_NAME = 'api.swagger.component'
    CONFIG_STORE_NAMES = ['swagger']
