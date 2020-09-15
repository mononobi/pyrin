# -*- coding: utf-8 -*-
"""
celery audit tasks module.
"""

import pyrin.task_queues.celery.audit.services as celery_audit_services

from pyrin.task_queues.celery.decorators import task


@task
def audit_task():
    """
    this method will be used to check status of celery.
    """

    celery_audit_services.perform_job()
