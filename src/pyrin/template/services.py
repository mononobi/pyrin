# -*- coding: utf-8 -*-
"""
template services module.
"""

from pyrin.application.services import get_component
from pyrin.template import TemplatePackage


def register_template_handler(instance, **options):
    """
    registers a new template handler or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a template handler which is already registered.

    :param AbstractTemplateHandler instance: template handler to be registered.
                                             it must be an instance of
                                             AbstractTemplateHandler.

    :keyword bool replace: specifies that if there is another registered
                           template handler with the same name, replace it
                           with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidTemplateHandlerTypeError: invalid template handler type error.
    :raises DuplicatedTemplateHandlerError: duplicated template handler error.
    """

    return get_component(TemplatePackage.COMPONENT_NAME).register_template_handler(instance,
                                                                                   **options)


def create(handler_name, *args, **kwargs):
    """
    creates the template using the given template handler name.

    :param str handler_name: handler name to be used.
    :param object args: arguments that should be passed to template handler.

    :keyword object kwargs: keyword arguments that should be passed to template handler.

    :raises TemplateHandlerNotFoundError: template handler not found error.
    """

    return get_component(TemplatePackage.COMPONENT_NAME).create(handler_name, *args, **kwargs)
