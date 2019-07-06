# -*- coding: utf-8 -*-
"""
localization decorators module.
"""


def timezone_selector():
    """
    decorator to register a timezone selector for application.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as timezone selector.

        :param callable func: function to register it as timezone selector.

        :rtype: callable
        """

        #application_services.register_error_handler(code_or_exception, func)

        return func

    return decorator
