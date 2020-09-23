# -*- coding: utf-8 -*-
"""
cli manager module.
"""

import colorama

import pyrin.utils.function as func_utils

from pyrin.cli import CLIPackage
from pyrin.cli.structs import CLIGroups
from pyrin.core.structs import Manager, CLI
from pyrin.utils.custom_print import print_colorful, print_error
from pyrin.cli.exceptions import InvalidCLIDecoratedMethodError, InvalidCLIGroupTypeError, \
    CLIGroupNameIsRequiredError, DuplicatedCLIGroupError


class CLIManager(Manager):
    """
    cli manager class.
    """

    package_class = CLIPackage

    def __init__(self):
        """
        initializes an instance of CLIManager.
        """

        super().__init__()

        self.__groups = CLIGroups()

    def register_cli_group(self, name, instance):
        """
        registers a cli group.

        :param str name: cli group name.
        :param CLI instance: cli group instance.

        :raises CLIGroupNameIsRequiredError: cli group name is required error.
        :raises DuplicatedCLIGroupError: duplicated cli group error.
        :raises InvalidCLIGroupTypeError: invalid cli group type error.
        """

        if name in (None, '') or name.isspace():
            raise CLIGroupNameIsRequiredError('CLI group name is required for '
                                              'registering cli group [{instance}].'
                                              .format(instance=instance))

        if hasattr(self.__groups, name) is True:
            raise DuplicatedCLIGroupError('There is another registered cli group with '
                                          'name [{name}]. so cli group [{instance}] '
                                          'could not be registered.'
                                          .format(name=name, instance=instance))

        if not isinstance(instance, CLI):
            raise InvalidCLIGroupTypeError('CLI group [{instance}] is not '
                                           'an instance of [{base}].'
                                           .format(instance=instance, base=CLI))

        setattr(self.__groups, name, instance)

    def get_cli_groups(self):
        """
        gets all registered cli groups.

        :rtype: CLIGroups
        """

        return self.__groups

    def process_function(self, func, func_args, func_kwargs):
        """
        processes the given cli handler function with given inputs.

        :param function func: function to to be executed.
        :param tuple func_args: a tuple of function positional inputs.
        :param dict func_kwargs: a dictionary of function keyword arguments.

        :raises CLIHandlerNotFoundError: cli handler not found error.
        :raises InvalidCLIDecoratedMethodError: invalid cli decorated method error.

        :rtype: int
        """

        try:
            inputs, cli_instance = func_utils.get_inputs(func, func_args, func_kwargs)
            func_kwargs.pop('help', None)
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

    def invoke_function(self, func, func_args, func_kwargs):
        """
        invokes the given function with given inputs.

        :param function func: function to be executed.
        :param tuple func_args: a tuple of function positional inputs.
        :param dict func_kwargs: a dictionary of function keyword arguments.

        :returns: function execution result.
        """

        try:
            inputs, parent = func_utils.get_inputs(func, func_args, func_kwargs)
            func_kwargs.pop('help', None)
            if self._process_help(func, inputs) is False:
                return func(*func_args, **func_kwargs)

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

        print_colorful(result, colorama.Fore.CYAN, force=True)

    def _process_help(self, func, inputs):
        """
        processes the function to print help message if required.

        :param function func: function to process help for it.
        :param dict inputs: a dict of function inputs.
        """

        if inputs.pop('help', False) is True:
            self._print_function_doc(func)
            return True

        return False
