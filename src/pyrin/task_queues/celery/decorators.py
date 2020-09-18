# -*- coding: utf-8 -*-
"""
celery decorators module.
"""

import pyrin.task_queues.celery.services as celery_services


# you could use this as decorator to register your tasks.
# you could also use celery's '@shared_task' decorator if you prefer.
task = celery_services.get_current_app().task
