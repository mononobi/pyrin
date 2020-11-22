# -*- coding: utf-8 -*-
"""
celery manager module.
"""

from celery import Celery

import pyrin.configuration.services as config_services
import pyrin.application.services as application_services

from pyrin.core.structs import Manager
from pyrin.task_queues.celery import CeleryPackage
from pyrin.task_queues.celery.structs import ExtendedTask


class CeleryManager(Manager):
    """
    celery manager class.
    """

    package_class = CeleryPackage
    task_class = ExtendedTask

    def __init__(self):
        """
        initializes an instance of CeleryManager.
        """

        super().__init__()

        self._app = self._configure()

    def _configure(self):
        """
        configures celery.
        """

        app = Celery(application_services.get_application_name(),
                     task_cls=self.task_class,
                     set_as_current=True)

        configs = config_services.get_active_section('celery')
        configs.update(worker_hijack_root_logger=False)
        app.config_from_object(configs)
        app.set_default()

        return app

    def get_current_app(self):
        """
        gets current celery application.

        :rtype: Celery
        """

        return self._app
