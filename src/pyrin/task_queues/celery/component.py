# -*- coding: utf-8 -*-
"""
celery component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.task_queues.celery import CeleryPackage
from pyrin.task_queues.celery.manager import CeleryManager


@component(CeleryPackage.COMPONENT_NAME)
class CeleryComponent(Component, CeleryManager):
    """
    celery component class.
    """
    pass
