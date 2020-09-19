# -*- coding: utf-8 -*-
"""
celery cli handlers events module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import CameraParam, \
    FrequencyParam, DumpParam, MaxRateParam


@celery_cli_handler()
class EventsCLIHandler(CeleryCLIHandlerBase):
    """
    events cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of EventsCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.EVENTS)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([CameraParam(), FrequencyParam(),
                       DumpParam(), MaxRateParam()])

        return super()._inject_params(params)
