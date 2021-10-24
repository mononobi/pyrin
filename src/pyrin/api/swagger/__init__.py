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
    COMPONENT_NAME = 'api.swagger.component'
    CONFIG_STORE_NAMES = ['swagger']
    DEPENDS = ['pyrin.api.router',
               'pyrin.configuration']
