# -*- coding: utf-8 -*-
"""
celery manager module.
"""

from celery import Celery
from celery.worker.worker import WorkController

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

        app = Celery(application_services.get_application_name(), task_cls=self.task_class)
        configs = config_services.get_active_section('celery')
        configs.update(worker_hijack_root_logger=False)
        app.config_from_object(configs)

        return app

    def _create_worker(self, **options):
        """
        creates a celery worker.

        :rtype: WorkController
        """

        return WorkController(self._app, **options)

    def get_current_app(self):
        """
        gets current celery application.

        :rtype: Celery
        """

        return self._app

    def start_worker(self, **options):
        """
        starts a celery worker.
        """

        worker = self._create_worker(**options)
        worker.start()
