# -*- coding: utf-8 -*-
"""
application enumerations module.
"""

from pyrin.core.enumerations import CoreEnum


class ApplicationStatusEnum(CoreEnum):
    """
    application status enum.
    """

    INITIALIZING = 'Initializing'
    LOADING = 'Loading'
    READY = 'Ready'
    RUNNING = 'Running'
    TERMINATED = 'Terminated'
