# -*- coding: utf-8 -*-
"""
logging masking hooks module.
"""

import pyrin.logging.masking.services as masking_services

from pyrin.logging.decorators import logging_hook
from pyrin.logging.hooks import LoggingHookBase


@logging_hook()
class LoggingHook(LoggingHookBase):
    """
    logging hook class.
    """

    def prepare_data(self, data, **options):
        """
        this method will be called when a log message interpolation is required.

        each subclass must return the modified or same input data.

        :param dict | object data: data that is passed to logging method.

        :returns: modified or same input data.
        :rtype: dict | object
        """

        return masking_services.mask(data, **options)
