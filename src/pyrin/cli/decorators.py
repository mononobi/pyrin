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
    decorated method must return a tuple containing two items.
    first item must be the relevant execute service with the following
    signature `execute(str handler_name, **inputs)` to be able to execute
    the cli handler. second item could be either a dict of modified
    inputs if required or None value.

    :param function func: function.

    :returns: decorated function.
    :rtype: function
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and executes the relevant cli handler.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.

        :raises CLIHandlerNotFoundError: cli handler not found error.

        :rtype: int
        """

        try:
            return cli_services.process_function(func, args, kwargs)

        except Exception as error:
            print_error('\n' + str(error), force=True)

    return update_wrapper(decorator, func)
