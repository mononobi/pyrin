# -*- coding: utf-8 -*-
"""
celery cli handlers report module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase


@celery_cli_handler()
class ReportCLIHandler(CeleryCLIHandlerBase):
    """
    report cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ReportCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.REPORT)
