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

    def __hash__(self):
        return hash(self.get_id())

    def __eq__(self, other):
        if not isinstance(other, PermissionMock):
            return False

        return other.get_id() == self.get_id()

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return '{id}-{description}'.format(id=self.get_id(), description=self.description)

    def __repr__(self):
        return str(self)

    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :rtype: PermissionEntity
        """

        entity = PermissionEntity(id=self.id, description=self.description)
        return entity

    def get_id(self):
        """
        gets permission id.
        note that this object must be fully unique for each different permission.

        :rtype: str
        """

        return self.id
