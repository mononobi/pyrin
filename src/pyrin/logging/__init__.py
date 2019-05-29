# -*- coding: utf-8 -*-
"""
logging package.
"""

from pyrin.packaging.base import Package


class LoggingPackage(Package):
    """
    logging package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'pyrin.logging.component'
