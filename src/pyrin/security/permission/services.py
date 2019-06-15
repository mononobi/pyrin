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
    :raises InvalidPermissionIDError: invalid permission id error.
    :raises DuplicatedPermissionError: duplicated permission error.
    """

    return get_component(PermissionPackage.COMPONENT_NAME).register_permission(instance,
                                                                               **options)
