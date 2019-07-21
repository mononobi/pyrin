# -*- coding: utf-8 -*-
"""
permission test_services module.
"""

import pytest

import pyrin.security.permission.services as permission_services
import pyrin.utils.unique_id as id_utils

from pyrin.security.permission.exceptions import DuplicatedPermissionError, \
    InvalidPermissionTypeError

from tests.security.permission.context import PermissionMock


def test_register_permission():
    """
    registers the given permission.
    """

    permission = PermissionMock(str(id_utils.generate_uuid4()))
    assert permission in permission_services.get_permissions()


def test_register_permission_duplicate():
    """
    registers the given permission which has been already registered.
    it should raise an error.
    """

    with pytest.raises(DuplicatedPermissionError):
        permission_id = str(id_utils.generate_uuid4())
        permission1 = PermissionMock(permission_id)
        permission2 = PermissionMock(permission_id)


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
