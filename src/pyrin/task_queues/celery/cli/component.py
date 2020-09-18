# -*- coding: utf-8 -*-
"""
celery cli component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.task_queues.celery.cli import CeleryCLIPackage
from pyrin.task_queues.celery.cli.manager import CeleryCLIManager


@component(CeleryCLIPackage.COMPONENT_NAME)
class CeleryCLIComponent(Component, CeleryCLIManager):
    """
    celery cli component class.
    """
    pass
