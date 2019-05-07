# -*- coding: utf-8 -*-
"""
packaging services module.
"""

from pyrin.packaging.component import PackagingComponent
from pyrin.application.services import get_component


def load_components(**options):
    """
    loads required packages and modules for application startup.
    """

    get_component(PackagingComponent.COMPONENT_ID).load_components(**options)


def load(module_name, **options):
    """
    loads the specified module.

    :param str module_name: module name.
                            example module_name = `pyrin.application.decorators`.

    :rtype: Module
    """

    return get_component(PackagingComponent.COMPONENT_ID).load(module_name, **options)
