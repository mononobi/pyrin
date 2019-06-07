# -*- coding: utf-8 -*-
"""
permissions services module.
"""

from pyrin.application.services import get_component
from pyrin.security.permissions import PermissionsPackage


def register_permission(instance, **options):
    """
    registers the given permission.

    :param PermissionBase instance: permission instance to be registered.

    :raises InvalidPermissionTypeError: invalid permission type error.
    :raises InvalidPermissionIDError: invalid permission id error.
    :raises DuplicatedPermissionError: duplicated permission error.
    """

    return get_component(PermissionsPackage.COMPONENT_NAME).register_permission(instance,
                                                                                **options)
