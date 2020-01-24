# -*- coding: utf-8 -*-
"""
datetime package.
"""

from pyrin.packaging.context import Package


class DateTimePackage(Package):
    """
    datetime package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'globalization.datetime.component'
    DEPENDS = ['pyrin.configuration']
