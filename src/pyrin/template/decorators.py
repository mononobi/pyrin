# -*- coding: utf-8 -*-
"""
template decorators module.
"""

import pyrin.template.services as template_services


def template_handler(**options):
    """
    decorator to register a template handler.

    :keyword bool replace: specifies that if there is another registered
                           template handler with the same name, replace it
                           with the new one, otherwise raise
                           an error. defaults to False.

    :raises InvalidTemplateHandlerTypeError: invalid template handler type error.
    :raises DuplicatedTemplateHandlerError: duplicated template handler error.

    :returns: template handler class.
    :rtype: AbstractTemplateHandler
    """

    def decorator(cls):
        """
        decorates the given class and registers an instance
        of it into available template handlers.

        :param AbstractTemplateHandler cls: template handler class.

        :returns: template handler class.
        :rtype: AbstractTemplateHandler
        """

        instance = cls()
        template_services.register_template_handler(instance, **options)

        return cls

    return decorator
