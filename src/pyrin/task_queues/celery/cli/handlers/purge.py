# -*- coding: utf-8 -*-
"""
celery cli handlers purge module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import ForceParam, ExcludeQueuesParam, \
    QueuesParam


@celery_cli_handler()
class PurgeCLIHandler(CeleryCLIHandlerBase):
    """
    purge cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of PurgeCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.PURGE)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([ForceParam(), QueuesParam(), ExcludeQueuesParam()])

        return super()._inject_params(params)
