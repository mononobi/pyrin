# -*- coding: utf-8 -*-
"""
permission context module.
"""

from pyrin.security.permission.base import PermissionBase


class PermissionMock(PermissionBase):
    """
    permission mock class.
    """

    def __init__(self, permission_id, **options):
        """
        initializes an instance of PermissionMock.

        :param str permission_id: permission unique id.
        """

        self._id = permission_id
        self.name = 'SamplePermission'

        PermissionBase.__init__(self, permission_id, **options)

    def __hash__(self):

        return hash(self.get_id())

    def __eq__(self, other):

        if not isinstance(other, PermissionMock):
            return False

        return other.get_id() == self.get_id()

    def __ne__(self, other):

        return not self == other

    def __str__(self):

        return '{id}-{name}'.format(id=self.get_id(), name=self.name)

    def __repr__(self):
        return str(self)

    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :rtype: CoreEntity
        """

        return None

    def get_id(self):
        """
        gets permission id.
        note that this object must be fully unique for each different permission.

        :rtype: str
        """

        return self._id
