# -*- coding: utf-8 -*-
"""
Packaging services.
"""

from bshop.core.packaging import manager


def load_components(**options):
    """
    Loads required packages and modules for application startup.
    """

    manager.load_components(**options)


def load(module_name, **options):
    """
    Loads the specified module.

    :param str module_name: module name.
                            example module_name = `bshop.core.application`.

    :rtype: Module
    """

    return manager.load(module_name, **options)
