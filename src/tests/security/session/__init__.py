# -*- coding: utf-8 -*-
"""
session package.
"""

from pyrin.packaging.context import Package


class SessionPackage(Package):
    """
    session package class.
    """

    NAME = __name__
    DEPENDS = []
    COMPONENT_NAME = 'security.session.component'
