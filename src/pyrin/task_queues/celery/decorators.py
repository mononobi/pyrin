# -*- coding: utf-8 -*-
"""
celery decorators module.
"""

import pyrin.task_queues.celery.services as celery_services


# you must use this as decorator to register your tasks. not the decorator of celery.
task = celery_services.get_current_app().task
