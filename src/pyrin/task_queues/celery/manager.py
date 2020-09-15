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

    def _create_workers(self, count=None, **options):
        """
        creates celery workers of given count.

        :param int count: number of workers to be created.
                          defaults to `celery` config store if not provided.

        :rtype: list[WorkController]
        """

        if count is None or count <= 0:
            # count = config_services.get_active('celery', '')
            count = 1

        workers = []
        for i in range(count):
            workers.append(self._create_worker(**options))

        return workers

    def get_current_app(self):
        """
        gets current celery application.

        :rtype: Celery
        """

        return self._app

    def start_workers(self, count=None, **options):
        """
        starts given number of celery workers.

        :param int count: number of workers to be created.
                          defaults to `celery` config store if not provided.
        """

        workers = self._create_workers(count, **options)
        for item in workers:
            item.start()
