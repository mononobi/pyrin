# -*- coding: utf-8 -*-
"""
mimetype services module.
"""

from pyrin.processor.mimetype import MIMETypePackage
from pyrin.application.services import get_component


def get_mimetype(value, **options):
    """
    gets the mimetype of given value.

    returns None if it could not detect the correct mimetype.

    :param object value: value to detect its mimetype.

    :returns: mimetype name
    :rtype: str
    """

    return get_component(MIMETypePackage.COMPONENT_NAME).get_mimetype(value, **options)


def register_mimetype_handler(instance, **options):
    """
    registers a new mimetype handler or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a mimetype handler which is already registered.

    :param AbstractMIMETypeHandlerBase instance: mimetype handler to be registered.
                                                 it must be an instance of
                                                 AbstractMIMETypeHandlerBase.

    :keyword bool replace: specifies that if there is another registered
                           mimetype handler with the same name and accepted type,
                           replace it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidMIMETypeHandlerTypeError: invalid mimetype handler type error.
    :raises DuplicatedMIMETypeHandlerError: duplicated mimetype handler error.
    """

    return get_component(MIMETypePackage.COMPONENT_NAME).register_mimetype_handler(instance,
                                                                                   **options)


def get_mimetype_handlers(**options):
    """
    gets all registered mimetype handlers.

    it could filter mimetype handlers for a specific type if provided.
    it only returns the first mimetype handlers for each type, because
    all mimetype handlers for a given type, are chained together.

    :keyword type accepted_type: specifies to get mimetype handlers which are
                                 registered for the accepted type. if not provided,
                                 all mimetype handlers will be returned.

    :rtype: list[AbstractMIMETypeHandlerBase]
    """

    return get_component(MIMETypePackage.COMPONENT_NAME).get_mimetype_handlers(**options)
