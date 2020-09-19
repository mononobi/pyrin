# -*- coding: utf-8 -*-
"""
celery cli handlers control module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import ControlMethodParam, \
    QueuePositionalParam, ExchangePositionalParam, ExchangeTypePositionalParam, \
    RoutingKeyPositionalParam, PoolResizeParam, MinScaleParam, MaxScaleParam, \
    RateLimitParam, SignalParam, SoftSecondsParam, HardSecondsParam, DestinationParam, \
    JSONParam, TimeoutParam, TaskNamePositionalParam, TaskIDListParam


@celery_cli_handler()
class ControlCLIHandler(CeleryCLIHandlerBase):
    """
    control cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ControlCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.CONTROL)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([ControlMethodParam(index=0),
                       QueuePositionalParam(index=1),
                       MaxScaleParam(index=1, validate_index=False),
                       PoolResizeParam(index=1, validate_index=False),
                       TaskNamePositionalParam(index=1, validate_index=False),
                       TaskIDListParam(index=1, validate_index=False),
                       SignalParam(index=1, validate_index=False),
                       ExchangePositionalParam(index=2),
                       MinScaleParam(index=2, validate_index=False),
                       RateLimitParam(index=2, validate_index=False),
                       TaskIDListParam(index=2, validate_index=False),
                       SoftSecondsParam(index=2, validate_index=False),
                       ExchangeTypePositionalParam(index=3),
                       HardSecondsParam(index=3, validate_index=False),
                       RoutingKeyPositionalParam(index=4),
                       TimeoutParam(), DestinationParam(), JSONParam()])

        return super()._inject_params(params)
