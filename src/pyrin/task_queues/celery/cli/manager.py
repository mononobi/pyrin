# -*- coding: utf-8 -*-
"""
celery cli manager module.
"""

from celery.bin.celery import CeleryCommand

import pyrin.task_queues.celery.services as celery_services

from pyrin.cli.mixin.handler import CLIMixin
from pyrin.core.structs import Manager
from pyrin.task_queues.celery.cli import CeleryCLIPackage
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase


class CeleryCLIManager(Manager, CLIMixin):
    """
    celery cli manager class.
    """

    _cli_handler_type = CeleryCLIHandlerBase
    package_class = CeleryCLIPackage

    def __init__(self):
        """
        initializes an instance of CeleryCLIManager.
        """

        super().__init__()
        self._command_executor = CeleryCommand(app=celery_services.get_current_app())

    def execute_on_celery(self, name, arguments=None):
        """
        executes the given celery command.

        :param str name: celery command name to be executed.
        :param list arguments: all command line arguments.

        :returns: result of celery command execution.
        """

        return self._command_executor.execute(name, arguments)
