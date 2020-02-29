# -*- coding: utf-8 -*-
"""
cli manager module.
"""

import inspect

import colorama

import pyrin.utils.function as func_utils

from pyrin.core.context import Manager
from pyrin.utils.custom_print import print_colorful


class CLIManager(Manager):
    """
    cli manager class.
    """

    def process_function(self, func, func_args, func_kwargs):
        """
        processes the given cli handler function with given inputs.

        :param function func: function to update its original inputs.
        :param tuple func_args: a tuple of function positional inputs.
        :param dict func_kwargs: a dictionary of function keyword arguments.
        """

        original_inputs = inspect.getcallargs(func, *func_args, **func_kwargs)
        original_inputs.pop('self', None)
        original_inputs.pop('cls', None)
        service, modified_inputs = func(*func_args, **func_kwargs)
        original_inputs.update(**(modified_inputs or {}))
        if self._process_help(func, original_inputs) is False:
            service.execute(func.__name__, **original_inputs)

    def _print_function_doc(self, func):
        """
        prints the docstring of given function.

        :param function func: function to print its docstring.
        """

        doc = func_utils.get_doc(func, False)
        result = '\n"{func}" command usage:\n\nyou could provide each ' \
                 'one of available\narguments with --argument format.\n\n' \
                 'command doc:\n{doc}' \
                 .format(func=func.__name__, doc=doc)

        print_colorful(result, colorama.Fore.CYAN, True)

    def _process_help(self, func, inputs):
        """
        processes the function to print help message if required.

        :param function func: function to process help for it.
        :param dict inputs: a dict of function inputs.
        """

        if inputs.get('help', False) is True:
            self._print_function_doc(func)
            return True

        return False
