# -*- coding: utf-8 -*-
"""
celery package.
"""

from pyrin.packaging.base import Package


class CeleryPackage(Package):
    """
    celery package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'task_queues.celery.component'
    CONFIG_STORE_NAMES = ['celery']
    DEPENDS = ['pyrin.configuration',
               'pyrin.logging']
