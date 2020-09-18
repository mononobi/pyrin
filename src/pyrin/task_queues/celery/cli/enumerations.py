# -*- coding: utf-8 -*-
"""
celery cli enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class CeleryCLIHandlersEnum(CoreEnum):
    """
    celery cli handlers enum.
    """

    AMQP = 'amqp'
    BEAT = 'beat'
    CALL = 'call'
    CONTROL = 'control'
    EVENTS = 'events'
    GRAPH = 'graph'
    HELP = 'help'
    LIST = 'list'
    INSPECT = 'inspect'
    LOGTOOL = 'logtool'
    MIGRATE = 'migrate'
    PURGE = 'purge'
    REPORT = 'report'
    RESULT = 'result'
    SHELL = 'shell'
    STATUS = 'status'
    UPGRADE = 'upgrade'
    WORKER = 'worker'
