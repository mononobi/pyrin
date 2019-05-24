# -*- coding: utf-8 -*-
"""
application decorators module.
"""

import pyrin.application.services as application_services

from pyrin.application.exceptions import InvalidComponentTypeError
from pyrin.context import Component


def component(*args, **kwargs):
    """
    decorator to register a component in application or replace the existing one
    if `replace=True` is provided. otherwise, it raises an error on adding an instance
    which it's id is already available in registered components.

    :param object args: component class constructor arguments.
    :param object kwargs: component class constructor keyword arguments.

    :keyword bool replace: specifies that if there is another registered
                           component with the same id, replace it with the new one.
                           otherwise raise an error. defaults to False.

    :raises InvalidComponentTypeError: invalid component type error.

    :returns: component class.

    :rtype: type
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available components of application.

        :param type cls: component class.

        :raises InvalidComponentTypeError: invalid component type error.

        :returns: component class.

        :rtype: type
        """

        if not issubclass(cls, Component):
            raise InvalidComponentTypeError('Input parameter [{class_name}] is '
                                            'not a subclass of Component.'
                                            .format(class_name=str(cls)))

        instance = cls(*args, **kwargs)
        application_services.register_component(instance, **kwargs)

        return cls

    return decorator


def error_handler(code_or_exception):
    """
    decorator to register an error handler for application.

    :param Union[int, Exception] code_or_exception: code or exception type to
                                                    register handler for.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as an error handler.

        :param callable func: function to register it as an error handler.

        :rtype: callable
        """

        application_services.register_error_handler(code_or_exception, func)

        return func

    return decorator


def before_request_handler():
    """
    decorator to register a function into application before request handlers.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it into application before request handlers.

        :param callable func: function to register it into application before request handlers.

        :rtype: callable
        """

        application_services.register_before_request_handler(func)

        return func

    return decorator


def after_request_handler():
    """
    decorator to register a function into application after request handlers.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it into application after request handlers.

        :param callable func: function to register it into application after request handlers.

        :rtype: callable
        """

        application_services.register_after_request_handler(func)

        return func

    return decorator


def route_factory():
    """
    decorator to register a function as application route factory.

    :rtype: callable
    """

    def decorator(func):
        """
        decorates the given function and registers it as application route factory.

        :param callable func: function to register it as application route factory.

        :rtype: callable
        """

        application_services.register_route_factory(func)

        return func

    return decorator
