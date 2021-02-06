# -*- coding: utf-8 -*-
"""
celery cli manager module.
"""

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
