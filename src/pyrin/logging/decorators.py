# -*- coding: utf-8 -*-
"""
logging decorators module.
"""

import time

from functools import update_wrapper

import pyrin.utils.function as func_utils
import pyrin.logging.services as logging_services
import pyrin.configuration.services as config_services


def audit(func):
    """
    decorator to log execution time of a function.

    :param function func: function.

    :returns: function result.
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and logs its execution time.

        note that `audit_log: true` is required in logging config
        store for each environment to enable this decorator.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :returns: function result.
        """

        if config_services.get_active('logging', 'audit_log') is not True:
            return func(*args, **kwargs)

        start_time = time.time()
        try:
            return func(*args, **kwargs)

        finally:
            end_time = time.time()
            logging_services.debug('Duration of function call [{name}]: [{time} ms].'
                                   .format(name=func_utils.get_fully_qualified_name(func),
                                           time='{:0.5f}'
                                           .format((end_time - start_time) * 1000)))

    return update_wrapper(decorator, func)


def logging_hook():
    """
    decorator to register a logging hook.

    :raises InvalidLoggingHookTypeError: invalid logging hook type error.

    :returns: logging hook class.
    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available logging hooks.

        :param type cls: logging hook class.

        :returns: logging hook class.
        :rtype: type
        """

        instance = cls()
        logging_services.register_hook(instance)

        return cls

    return decorator
