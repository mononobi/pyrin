# -*- coding: utf-8 -*-
"""
celery cli handlers amqp module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase


@celery_cli_handler()
class AMQPCLIHandler(CeleryCLIHandlerBase):
    """
    amqp cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of AMQPCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.AMQP)
