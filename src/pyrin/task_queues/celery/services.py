# -*- coding: utf-8 -*-
"""
celery services module.
"""

from pyrin.application.services import get_component
from pyrin.task_queues.celery import CeleryPackage


def get_current_app():
    """
    gets current celery application.

    :rtype: Celery
    """

    return get_component(CeleryPackage.COMPONENT_NAME).get_current_app()
