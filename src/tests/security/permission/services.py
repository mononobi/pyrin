# -*- coding: utf-8 -*-
"""
permission services module.
"""

from pyrin.application.services import get_component
from pyrin.security.permission import PermissionPackage


def register_permission(instance, **options):
    """
    registers the given permission.

    :param PermissionBase instance: permission instance to be registered.

    :raises InvalidPermissionTypeError: invalid permission type error.
    :raises DuplicatedPermissionError: duplicated permission error.
    """

    return get_component(PermissionPackage.COMPONENT_NAME).register_permission(instance,
                                                                               **options)


def get_permissions(**options):
    """
    gets all registered permissions.

    :rtype: list[PermissionBase]
    """

    return get_component(PermissionPackage.COMPONENT_NAME).get_permissions(**options)


def synchronize_all(**options):
    """
    synchronizes all permissions with database.
    """

    return get_component(PermissionPackage.COMPONENT_NAME).synchronize_all(**options)
