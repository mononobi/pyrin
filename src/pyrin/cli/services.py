# -*- coding: utf-8 -*-
"""
cli services module.
"""

from pyrin.application.services import get_component
from pyrin.cli import CLIPackage


def register_cli_group(name, instance):
    """
    registers a cli group.

    :param str name: cli group name.
    :param CLI instance: cli group instance.

    :raises CLIGroupNameIsRequiredError: cli group name is required error.
    :raises DuplicatedCLIGroupError: duplicated cli group error.
    :raises InvalidCLIGroupTypeError: invalid cli group type error.
    """

    return get_component(CLIPackage.COMPONENT_NAME).register_cli_group(name, instance)


def get_cli_groups():
    """
    gets all registered cli groups.

    :rtype: CLIGroups
    """

    return get_component(CLIPackage.COMPONENT_NAME).get_cli_groups()


def process_function(func, func_args, func_kwargs):
    """
    processes the given cli handler function with given inputs.

    :param function func: function to be executed.
    :param tuple func_args: a tuple of function positional inputs.
    :param dict func_kwargs: a dictionary of function keyword arguments.

    :raises CLIHandlerNotFoundError: cli handler not found error.
    :raises InvalidCLIDecoratedMethodError: invalid cli decorated method error.

    :rtype: int
    """

    return get_component(CLIPackage.COMPONENT_NAME).process_function(func, func_args,
                                                                     func_kwargs)


def invoke_function(func, func_args, func_kwargs):
    """
    invokes the given function with given inputs.

    :param function func: function to be executed.
    :param tuple func_args: a tuple of function positional inputs.
    :param dict func_kwargs: a dictionary of function keyword arguments.

    :returns: function execution result.
    """

    return get_component(CLIPackage.COMPONENT_NAME).invoke_function(func, func_args,
                                                                    func_kwargs)
