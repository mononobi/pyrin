# -*- coding: utf-8 -*-
"""
celery decorators module.
"""

import pyrin.task_queues.celery.services as celery_services


# this is a workaround to overcome the problem of '@shared_task' not
# finding the celery app. you must use this as decorator to register your tasks.
task = celery_services.get_current_app().task
