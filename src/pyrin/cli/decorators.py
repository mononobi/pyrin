# -*- coding: utf-8 -*-
"""
cli decorators module.
"""

from functools import update_wrapper

import pyrin.cli.services as cli_services

from pyrin.utils.custom_print import print_error


def cli(func):
    """
    decorator to specify a method that handles a cli command.

    the method name will be used as the handler name for that cli handler.
    the decorated method, will be get called if `help=True` is not in options,
    so you could do something in the decorated method body if required.
    but it's highly recommended that do not do any complex operation inside
    cli handler methods, instead implement the required operations in the manager
    of relevant package and just call the relevant service inside the cli method.

    :param function func: function.

    :raises CLIHandlerNotFoundError: cli handler not found error.
    :raises InvalidCLIDecoratedMethodError: invalid cli decorated method error.

    :returns: decorated function.
    :rtype: function
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and executes the relevant cli handler.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :raises CLIHandlerNotFoundError: cli handler not found error.
        :raises InvalidCLIDecoratedMethodError: invalid cli decorated method error.

        :rtype: int
        """

        try:
            return cli_services.process_function(func, args, kwargs)

        except Exception as error:
            print_error(str(error), force=True)

    return update_wrapper(decorator, func)
