# -*- coding: utf-8 -*-
"""
celery audit package.
"""

from pyrin.packaging.base import Package


class CeleryAuditPackage(Package):
    """
    celery audit package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'task_queues.celery.audit.component'
    DEPENDS = ['pyrin.audit']
