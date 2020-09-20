# -*- coding: utf-8 -*-
"""
celery cli handlers logtool module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import ActionParam, FilesParam


@celery_cli_handler()
class LogToolCLIHandler(CeleryCLIHandlerBase):
    """
    logtool cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of LogToolCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.LOGTOOL)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([ActionParam(index=0), FilesParam(index=1)])

        return super()._inject_params(params)
