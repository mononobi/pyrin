# -*- coding: utf-8 -*-
"""
token package.
"""

from pyrin.packaging.base import Package


class TokenPackage(Package):
    """
    token package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.token.component'
