# -*- coding: utf-8 -*-
"""
celery cli handlers list module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import TopicParam


@celery_cli_handler()
class ListCLIHandler(CeleryCLIHandlerBase):
    """
    list cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of ListCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.LIST)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([TopicParam(index=0)])

        return super()._inject_params(params)
