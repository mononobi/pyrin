# -*- coding: utf-8 -*-
"""
security permissions module.
"""

import pyrin.utils.unique_id as unique_id_utils

from tests.security.permission.context import PermissionMock


PERMISSION_TEST_ONE = PermissionMock(str(unique_id_utils.generate_uuid4()))
PERMISSION_TEST_TWO = PermissionMock(str(unique_id_utils.generate_uuid4()))
PERMISSION_TEST_THREE = PermissionMock(str(unique_id_utils.generate_uuid4()))
PERMISSION_TEST_FOUR = PermissionMock(str(unique_id_utils.generate_uuid4()))
PERMISSION_TEST_FIVE = PermissionMock(str(unique_id_utils.generate_uuid4()))
