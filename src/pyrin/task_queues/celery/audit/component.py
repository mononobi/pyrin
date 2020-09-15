# -*- coding: utf-8 -*-
"""
celery audit component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.task_queues.celery.audit import CeleryAuditPackage
from pyrin.task_queues.celery.audit.manager import CeleryAuditManager


@component(CeleryAuditPackage.COMPONENT_NAME)
class CeleryAuditComponent(Component, CeleryAuditManager):
    """
    celery audit component class.
    """
    pass
