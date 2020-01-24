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
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'logging.component'
    CONFIG_STORE_NAMES = ['logging']
    LOGGER_HANDLERS_STORE_NAME = 'logging.handlers'
