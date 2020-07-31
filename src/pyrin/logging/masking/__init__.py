# -*- coding: utf-8 -*-
"""
logging masking package.
"""

from pyrin.packaging.base import Package


class LoggingMaskingPackage(Package):
    """
    logging masking package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
    COMPONENT_NAME = 'logging.masking.component'
    CONFIG_STORE_NAMES = ['logging.masking']
