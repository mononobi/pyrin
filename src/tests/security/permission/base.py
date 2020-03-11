# -*- coding: utf-8 -*-
"""
permission base module.
"""

from pyrin.security.permission.base import PermissionBase

from tests.security.permission.models import PermissionEntity


class PermissionMock(PermissionBase):
    """
    permission mock class.
    """

    def __init__(self, permission_id, description, **options):
        """
        initializes an instance of PermissionMock.

        :param int permission_id: permission id.
        :param str description: permission description.
        """

        self.id = permission_id
        self.description = description

        super().__init__(**options)

    def __str__(self):
        return '{id}-{description}'.format(id=self.get_id(), description=self.description)

    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :rtype: PermissionEntity
        """

        return PermissionEntity(id=self.id, description=self.description)

    def get_id(self):
        """
        gets permission id.

        :rtype: int
        """

        return self.id
