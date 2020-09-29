# -*- coding: utf-8 -*-
"""
locale package.
"""

from pyrin.packaging.base import Package


class LocalePackage(Package):
    """
    locale package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'globalization.locale.component'
    DEPENDS = ['pyrin.configuration']
