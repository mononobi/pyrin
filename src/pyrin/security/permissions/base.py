# -*- coding: utf-8 -*-
"""
permissions base module.
"""

import pyrin.security.permissions.services as permission_services

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class PermissionBase(CoreObject):
    """
    permission base class.
    all application permissions must be subclassed from this.
    """

    def __init__(self, permission_id, description, **options):
        """
        initializes an instance of PermissionBase.

        :param object permission_id: permission id.
                                     it must be an immutable type to
                                     be usable as dict key.

        :param str description: permission description.
        """

        CoreObject.__init__(self)

        self._id = permission_id
        self.description = description

        permission_services.register_permission(self, **options)

    def __hash__(self):
        """
        this method must be implemented in all subclasses to
        calculate the correct hash of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    def __str__(self):
        """
        this method must be implemented in all subclasses to
        get the correct string representation of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def get_id(self):
        """
        gets permission id.
        it must be an immutable type to be usable as dict key.

        :rtype: object
        """

        return self._id

    def synchronize(self, **options):
        """
        synchronizes the current permission object with database.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()
