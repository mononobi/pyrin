# -*- coding: utf-8 -*-
"""
model package.
"""

from pyrin.packaging.context import Package


class DatabaseModelPackage(Package):
    """
    database model package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.database.session_factory']
