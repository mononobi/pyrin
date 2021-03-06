# -*- coding: utf-8 -*-
"""
celery cli handlers result module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import TaskIDParam, \
    TaskNameParam, TracebackParam


@celery_cli_handler()
class ResultCLIHandler(CeleryCLIHandlerBase):
    """
    result cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ResultCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.RESULT)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([TaskIDParam(index=0), TaskNameParam(), TracebackParam()])

        return super()._inject_params(params)
