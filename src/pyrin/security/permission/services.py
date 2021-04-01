# -*- coding: utf-8 -*-
"""
permission services module.
"""

from pyrin.application.services import get_component
from pyrin.database.transaction.decorators import atomic
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


@atomic(expire_on_commit=True)
def synchronize_all(**options):
    """
    synchronizes all permissions with database.

    it creates or updates the available permissions.
    """

    return get_component(PermissionPackage.COMPONENT_NAME).synchronize_all(**options)
