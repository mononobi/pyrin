# -*- coding: utf-8 -*-
"""
celery cli handlers status module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import TimeoutParam, JSONParam, \
    DestinationParam


@celery_cli_handler()
class StatusCLIHandler(CeleryCLIHandlerBase):
    """
    status cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of StatusCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.STATUS)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([TimeoutParam(), DestinationParam(), JSONParam()])

        return super()._inject_params(params)
