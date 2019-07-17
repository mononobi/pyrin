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
        PermissionBase.__init__(self, permission_id, **options)

    def __hash__(self):

        return hash(self._id)

    def __eq__(self, other):

        return other.get_id() == self.get_id()

    def __str__(self):

        return str(self._id)

    def synchronize(self, **options):
        """
        synchronizes the current permission object with database.
        """
        pass

    def get_id(self):
        """
        gets permission id.

        :rtype: str
        """

        return self._id
