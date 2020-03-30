# -*- coding: utf-8 -*-
"""
session package.
"""

from pyrin.security.session import SessionPackage as BaseSessionPackage


class SessionPackage(BaseSessionPackage):
    """
    session package class.
    """

    NAME = __name__
