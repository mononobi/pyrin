# -*- coding: utf-8 -*-
"""
cli decorators module.
"""

import inspect

from functools import update_wrapper

import pyrin.database.migration.alembic.services as alembic_services

from pyrin.utils.custom_print import print_error


def cli(func):
    """
    decorator to specify a method that handles a cli command.
    the method name will be used as the handler name for that cli handler.
    decorated method could modify inputs and return a dict of modified
    inputs if required.

    :param callable func: function.

    :returns: decorated function.
    :rtype: callable
    """

    def decorator(*args, **kwargs):
        """
        decorates the given function and executes the relevant cli handler.

        :param object args: function arguments.
        :param object kwargs: function keyword arguments.
        """

        try:
            original_inputs = inspect.getcallargs(func, *args, **kwargs)
            original_inputs.pop('self', None)
            original_inputs.pop('cls', None)
            modified_inputs = func(*args, **kwargs)
            original_inputs.update(**(modified_inputs or {}))
            alembic_services.execute(func.__name__, **original_inputs)

        except Exception as error:
            print_error(str(error), force=True)

    return update_wrapper(decorator, func)
