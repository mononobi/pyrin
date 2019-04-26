# -*- coding: utf-8 -*-
"""
Application services.
"""

from bshop.core.application import app


def add_context(key, value):
    """
    Adds the given key and it's value into the application context.

    :param str key: related key for storing application context.
    :param object value: related value for storing in application context.
    """

    app.add_context(key, value)


def get_context(key):
    """
    Gets the application context value that belongs to given key.

    :param str key: key for requested application context.

    :rtype: object
    """

    return app.get_context(key)


def register_component(component, **options):
    """
    Registers given application component.

    :param Component component: component instance.
    """

    app.register_component(component, **options)


def get_component(component_id, **options):
    """
    Gets the specified application component.

    :param str component_id: component unique id.

    :rtype: Component
    """

    return app.get_component(component_id, **options)
