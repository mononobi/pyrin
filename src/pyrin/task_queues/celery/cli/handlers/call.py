# -*- coding: utf-8 -*-
"""
celery cli handlers call module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import TaskNamePositionalParam, \
    ArgsParam, KwargsParam, ETAParam, CountdownParam, ExpiresParam, SerializerParam, \
    QueueParam, ExchangeParam, RoutingKeyParam


@celery_cli_handler()
class CallCLIHandler(CeleryCLIHandlerBase):
    """
    call cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of CallCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.CALL)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([TaskNamePositionalParam(index=0),
                       ArgsParam(), KwargsParam(),
                       ETAParam(), CountdownParam(),
                       ExpiresParam(), SerializerParam(),
                       QueueParam(), ExchangeParam(),
                       RoutingKeyParam()])

        return super()._inject_params(params)
