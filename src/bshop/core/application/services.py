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
    registers given application component or replaces the existing one
    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's id is already available
    in registered components.

    :param Component component: component instance.

    :keyword bool replace: specifies that if there is another registered
                           component with the same id, replace it with the new one.
                           otherwise raise an error. defaults to False.
    """

    _get_app().register_component(component, **options)


def get_component(component_id, **options):
    """
    gets the specified application component.

    :param str component_id: component unique id.

    :rtype: Component
    """

    return _get_app().get_component(component_id, **options)


def register_error_handler(code_or_exception, func):
    """
    registers the given function as an error handler for given code or exception type.

    :param Union[int, Exception] code_or_exception: code or exception to register error handler for.
    :param callable func: function to register it as an error handler.
    """

    _get_app().register_error_handler(code_or_exception, func)


def register_before_request_handler(func):
    """
    registers the given function into application before request handlers.

    :param callable func: function to register it into before request handlers.
    """

    _get_app().before_request(func)


def register_after_request_handler(func):
    """
    registers the given function into application after request handlers.

    :param callable func: function to register it into after request handlers.
    """

    _get_app().after_request(func)
