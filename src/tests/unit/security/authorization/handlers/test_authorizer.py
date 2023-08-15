# -*- coding: utf-8 -*-
"""
authorization test authorizers package.
"""

import pyrin.utils.misc as misc_utils

from pyrin.security.authorization.decorators import authorizer
from pyrin.security.authorization.handlers.base import AuthorizerBase

from tests.unit.security.permissions import PERMISSION_TEST_ONE, PERMISSION_TEST_TWO, \
    PERMISSION_TEST_THREE


@authorizer()
class UnitTestAuthorizer(AuthorizerBase):
    """
    unit test authorizer class.
    """

    _name = 'test'

    def _has_permission(self, user, permissions, **options):
        """
        gets a value indicating that given user has the requested permissions.

        :param user: user identity to authorize permissions for.
        :param tuple[PermissionBase] permissions: permissions to check for user authorization.

        :keyword dict user_info: user info to be used for authorization.

        :rtype: bool
        """

        required_permissions = permissions
        required_permissions = misc_utils.make_iterable(required_permissions, list)
        needed_permissions = set(required_permissions)
        user_permissions = {PERMISSION_TEST_ONE,
                            PERMISSION_TEST_TWO,
                            PERMISSION_TEST_THREE}

        return needed_permissions.issubset(user_permissions)
