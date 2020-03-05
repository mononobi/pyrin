# -*- coding: utf-8 -*-
"""
cli manager module.
"""

import inspect

import colorama

import pyrin.utils.function as func_utils

from pyrin.core.context import Manager
from pyrin.utils.custom_print import print_colorful, print_error
from pyrin.cli.exceptions import InvalidCLIDecoratedMethodError


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

        :raises CLIHandlerNotFoundError: cli handler not found error.
        :raises InvalidCLIDecoratedMethodError: invalid cli decorated method error.

        :rtype: int
        """

        try:
            signature = inspect.signature(func)
            bounded_args = signature.bind_partial(*func_args, **func_kwargs)
            inputs = dict(**bounded_args.kwargs)
            inputs.update(**bounded_args.arguments)

            inputs.pop('cls', None)
            cli_instance = inputs.pop('self', None)
            if cli_instance is None:
                raise InvalidCLIDecoratedMethodError('The "@cli" decorator must '
                                                     'be set on instance methods. '
                                                     'static methods or stand-alone '
                                                     'functions are not valid.')

            if self._process_help(func, inputs) is False:
                func(*func_args, **func_kwargs)
                return cli_instance.execute(func.__name__, **inputs)

        except TypeError as error:
            print_error(str(error) + '\n', force=True)
            self._print_function_doc(func)

    def _print_function_doc(self, func):
        """
        prints the docstring of given function.

        :param function func: function to print its docstring.
        """

        doc = func_utils.get_doc(func, False)
        if doc is not None and len(doc) > 0:
            result = '`{func}` command usage:\n\neach argument could be passed ' \
                     'with `--arg value` format\nor all arguments could be passed in ' \
                     'positional order.\nfor boolean arguments, you just need to pass ' \
                     '`--arg` without any \nvalue for True and do not pass it to use ' \
                     'default value (often False).\n\n`{func}` command doc:\n\n{doc}' \
                     .format(func=func.__name__, doc=doc)
        else:
            result = '`{func}` command help is not available.'.format(func=func.__name__)

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
