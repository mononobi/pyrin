# -*- coding: utf-8 -*-
"""
template package.
"""

from pyrin.packaging.base import Package


class TemplatePackage(Package):
    """
    template package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'template.component'
    DEPENDS = ['pyrin.cli']
