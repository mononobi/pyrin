# -*- coding: utf-8 -*-
"""
cli core services module.
"""

from pyrin.cli.core.manager import CLICoreManager


def get_manager():
    """
    gets the cli core manager instance.

    :rtype: CLICoreManager
    """

    return CLICoreManager()


def create(handler_name):
    """
    creates the required templates using relevant handlers.

    :param str handler_name: handler name to be used.

    :raises CLICoreTemplateHandlerNotFoundError: cli core template handler not found error.
    """

    return get_manager().create(handler_name)
