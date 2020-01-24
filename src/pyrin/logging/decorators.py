# -*- coding: utf-8 -*-
"""
logging decorators module.
"""

import time

from functools import update_wrapper

import pyrin.logging.services as logging_services
import pyrin.configuration.services as config_services


def audit(func):
    """
    decorator to log information before and after
    a function execution in debug mode.

    :param callable func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and logs it's behavior in debug mode
        and returns the function's result every time that function gets called.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        if config_services.get_active('logging', 'audit_log') is not True:
            return func(*args, **kwargs)

        start_time = time.time()
        try:
            return func(*args, **kwargs)

        except Exception as ex:
            raise ex
        finally:
            end_time = time.time()
            logging_services.debug('Duration of function call [{name}]: [{time} ms].'
                                   .format(name=func.__name__,
                                           time='{:0.5f}'
                                           .format((end_time - start_time) * 1000)))

    return update_wrapper(decorator, func)
