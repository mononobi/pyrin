# -*- coding: utf-8 -*-
"""
celery cli handlers shell module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import IPythonParam, \
    BPythonParam, PythonParam, WithoutTasksParam, EventletParam, GeventParam


@celery_cli_handler()
class ShellCLIHandler(CeleryCLIHandlerBase):
    """
    shell cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ShellCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.SHELL)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([IPythonParam(), BPythonParam(), PythonParam(),
                       WithoutTasksParam(), EventletParam(), GeventParam()])

        return super()._inject_params(params)
