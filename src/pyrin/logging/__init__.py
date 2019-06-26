# -*- coding: utf-8 -*-
"""
logging package.
"""

from pyrin.packaging.context import Package


class LoggingPackage(Package):
    """
    logging package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration',
               'pyrin.database']

    COMPONENT_NAME = 'logging.component'
