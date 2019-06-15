# -*- coding: utf-8 -*-
"""
application enumerations module.
"""

from pyrin.core.context import CoreEnum


class ApplicationStatusEnum(CoreEnum):
    """
    application status enum.
    """

    INITIALIZING = 'Initializing'
    LOADING = 'Loading'
    RUNNING = 'Running'
    TERMINATED = 'Terminated'
