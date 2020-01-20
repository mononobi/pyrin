# -*- coding: utf-8 -*-
"""
permission test_services module.
"""

import pytest

import pyrin.security.permission.services as permission_services

from pyrin.security.permission.exceptions import DuplicatedPermissionError, \
    InvalidPermissionTypeError

from tests.security.permission.base import PermissionMock


def test_register_permission():
    """
    registers the given permission.
    """

    permission = PermissionMock(11, 'permission_11')
    assert permission in permission_services.get_permissions()


def test_register_permission_duplicate():
    """
    registers the given permission which has been already registered.
    it should raise an error.
    """

    with pytest.raises(DuplicatedPermissionError):
        permission_id = 10
        permission1 = PermissionMock(permission_id, 'permission_10')
        permission2 = PermissionMock(permission_id, 'permission_10_duplicate')


def test_register_permission_invalid_type():
    """
    registers the given permission which has an invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidPermissionTypeError):
        permission_services.register_permission(object())


def test_get_permissions():
    """
    gets all registered permissions.
    """

    permissions = permission_services.get_permissions()
    assert len(permissions) > 3
