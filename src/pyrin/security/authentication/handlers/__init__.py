# -*- coding: utf-8 -*-
"""
authentication handlers package.
"""

from pyrin.packaging.base import Package


class AuthenticationHandlersPackage(Package):
    """
    authentication handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.users.internal']
