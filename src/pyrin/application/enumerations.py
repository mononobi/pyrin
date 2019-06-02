# -*- coding: utf-8 -*-
"""
application enumerations module.
"""

from pyrin.core.context import CoreEnum


class ApplicationStatusEnum(CoreEnum):
    """
    application status enum.
    """

    # application is initializing.
    INITIALIZING = 'Initializing'

    # application is loading.
    LOADING = 'Loading'

    # application is running.
    RUNNING = 'Running'

    # application is terminated.
    TERMINATED = 'Terminated'
