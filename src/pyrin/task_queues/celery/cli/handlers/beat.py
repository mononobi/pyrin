# -*- coding: utf-8 -*-
"""
celery cli handlers beat module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import BeatLogFileParam, \
    BeatPIDFileParam, BeatLogLevelParam


@celery_cli_handler()
class BeatCLIHandler(CeleryCLIHandlerBase):
    """
    beat cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of BeatCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.BEAT)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([BeatLogFileParam(), BeatPIDFileParam(), BeatLogLevelParam()])

        return super()._inject_params(params)
