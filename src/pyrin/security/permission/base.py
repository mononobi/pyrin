# -*- coding: utf-8 -*-
"""
permission base module.
"""

import pyrin.security.permission.services as permission_services

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class PermissionBase(CoreObject):
    """
    permission base class.
    all application permissions must be subclassed from this.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of PermissionBase.
        """

        CoreObject.__init__(self)
        permission_services.register_permission(self, **options)

    def __hash__(self):
        """
        this method must be implemented in all subclasses to
        calculate the correct hash of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    def __eq__(self, other):
        """
        this method must be implemented in all subclasses to get the correct
        comparison between current and other permission.

        :param PermissionBase other: other permission instance to be
                                     compared to the current one.

        :raises CoreNotImplementedError: core not implemented error.
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

    def __repr__(self):
        """
        this method must be implemented in all subclasses to
        get the correct string representation of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        :return:
        """

        raise CoreNotImplementedError()

    def synchronize(self, **options):
        """
        synchronizes the current permission object with database.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    def get_id(self):
        """
        gets permission id.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()
