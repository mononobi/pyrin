# -*- coding: utf-8 -*-
"""
application services module.
"""

from bshop.core import _get_app


def add_context(key, value):
    """
    adds the given key and it's value into the application context.

    :param str key: related key for storing application context.
    :param object value: related value for storing in application context.
    """

    _get_app().add_context(key, value)


def get_context(key):
    """
    gets the application context value that belongs to given key.

    :param str key: key for requested application context.

    :rtype: object
    """

    return _get_app().get_context(key)


def register_component(component, **options):
    """
    registers given application component.

    :param Component component: component instance.
    """

    _get_app().register_component(component, **options)


def get_component(component_id, **options):
    """
    gets the specified application component.

    :param str component_id: component unique id.

    :rtype: Component
    """

    return _get_app().get_component(component_id, **options)
