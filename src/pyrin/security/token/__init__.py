# -*- coding: utf-8 -*-
"""
token package.
"""

from pyrin.packaging import Package


class TokenPackage(Package):
    """
    token package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'pyrin.security.token.component'