# -*- coding: utf-8 -*-
"""
logging decorators module.
"""

import time

from functools import update_wrapper

import pyrin.logging.services as logging_services

from pyrin.settings.static import AUDIT_LOG


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

        if not AUDIT_LOG:
            return func(*args, **kwargs)

        start_time = time.time()
        try:
            return func(*args, **kwargs)

        except Exception as ex:
            raise ex
        finally:
            end_time = time.time()
            logging_services.debug('Duration of function call [{name}]: {milliseconds} ms'
                                   .format(name=func.__name__,
                                           milliseconds=(end_time - start_time) * 1000))

    return update_wrapper(decorator, func)
