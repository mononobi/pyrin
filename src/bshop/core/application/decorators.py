# -*- coding: utf-8 -*-
"""
Application decorators module.
"""

import bshop.core.application.services as application_services

from bshop.core.context import Component
from bshop.core.exceptions import CoreTypeError


def register_component(*args, **kwargs):
    """
    Decorator to register a component to application.

    :param object args: component class constructor arguments.
    :param object kwargs: component class constructor keyword arguments.

    :returns: component class.

    :rtype: type
    """

    def decorator(cls):
        """
        Decorates the given class and registers an instance
        of it into available components of application.

        :param type cls: component class.

        :raises CoreTypeError: core type error.

        :returns: component class.

        :rtype: type
        """

        if not issubclass(cls, Component):
            raise CoreTypeError('Input parameter [{class_name}] is '
                                'not a subclass of Component.'
                                .format(class_name=str(cls)))

        instance = cls(*args, **kwargs)
        application_services.register_component(instance)

        return cls

    return decorator
