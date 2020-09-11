# -*- coding: utf-8 -*-
"""
sentry package.
"""

from pyrin.packaging.base import Package


class SentryPackage(Package):
    """
    sentry package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'logging.sentry.component'
    CONFIG_STORE_NAMES = ['sentry']
    DEPENDS = ['pyrin.configuration',
               'pyrin.api']
