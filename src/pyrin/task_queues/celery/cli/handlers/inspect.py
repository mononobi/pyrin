# -*- coding: utf-8 -*-
"""
celery cli handlers inspect module.
"""

from pyrin.task_queues.celery.cli.decorators import celery_cli_handler
from pyrin.task_queues.celery.cli.enumerations import CeleryCLIHandlersEnum
from pyrin.task_queues.celery.cli.interface import CeleryCLIHandlerBase
from pyrin.task_queues.celery.cli.handlers.params import InspectMethodParam, \
    TimeoutParam, DestinationParam, JSONParam, IncludeDefaultsParam, SamplesCountParam, \
    ObjectTypeParam, CountParam, MaxDepthParam, TaskIDListParam, AttributeListParam


@celery_cli_handler()
class InspectCLIHandler(CeleryCLIHandlerBase):
    """
    inspect cli handler class.
    """

    def __init__(self):
        """
        initializes an instance of InspectCLIHandler.
        """

        super().__init__(CeleryCLIHandlersEnum.INSPECT)

    def _inject_params(self, params):
        """
        injects all the params of current handler into given list.

        :param list[CLIParamBase] params: list of all params.
        """

        params.extend([InspectMethodParam(index=0), IncludeDefaultsParam(index=1),
                       SamplesCountParam(index=1, validate_index=False),
                       ObjectTypeParam(index=1, validate_index=False),
                       TaskIDListParam(index=1, validate_index=False),
                       AttributeListParam(index=1, validate_index=False),
                       CountParam(index=2), MaxDepthParam(index=3),
                       TimeoutParam(), DestinationParam(), JSONParam()])

        return super()._inject_params(params)
