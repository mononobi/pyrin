# -*- coding: utf-8 -*-
"""
swagger services module.
"""

from pyrin.application.services import get_component
from pyrin.api.swagger import SwaggerPackage


def register_tag(instance, **options):
    """
    registers a new tag or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding a tag which is already registered.

    :param AbstractTag instance: tag to be registered.
                                 it must be an instance of AbstractTag.

    :keyword bool replace: specifies that if there is another registered
                           tag with the same name, replace it with the
                           new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidTagTypeError: invalid tag type error.
    :raises DuplicatedTagError: duplicated tag error.
    """

    return get_component(SwaggerPackage.COMPONENT_NAME).register_tag(instance, **options)


def get_tags(rule, method, **options):
    """
    gets the valid tags for given rule.

    :param pyrin.api.router.handlers.base.RouteBase rule: rule instance to be processed.
    :param str method: http method name.

    :rtype: list[str]
    """

    return get_component(SwaggerPackage.COMPONENT_NAME).get_tags(rule, method, **options)
