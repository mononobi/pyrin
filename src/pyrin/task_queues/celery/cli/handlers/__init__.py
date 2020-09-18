# -*- coding: utf-8 -*-
"""
celery cli handlers package.
"""

from pyrin.packaging.base import Package


class CeleryCLIHandlersPackage(Package):
    """
    celery cli handlers package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.configuration']
