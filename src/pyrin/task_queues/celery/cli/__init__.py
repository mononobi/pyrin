# -*- coding: utf-8 -*-
"""
celery cli package.
"""

from pyrin.packaging.base import Package


class CeleryCLIPackage(Package):
    """
    celery cli package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'task_queues.celery.cli.component'
    DEPENDS = ['pyrin.cli']
