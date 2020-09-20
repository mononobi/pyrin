# -*- coding: utf-8 -*-
"""
celery cli handlers worker module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import ConcurrencyParam, \
    PurgeParam, BeatParam, HostnameParam, AutoScaleParam, WorkerLogFileParam, \
    WorkerPIDFileParam, WorkerLogLevelParam, OptimizationParam, WorkerQueuesParam


@celery_cli_handler()
class WorkerCLIHandler(CeleryCLIHandlerBase):
    """
    worker cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of WorkerCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.WORKER)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([ConcurrencyParam(), PurgeParam(), BeatParam(),
                       HostnameParam(), AutoScaleParam(), WorkerLogFileParam(),
                       WorkerPIDFileParam(), WorkerLogLevelParam(), WorkerQueuesParam(),
                       OptimizationParam()])

        return super()._inject_params(params)
