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

        super().__init__()
        permission_services.register_permission(self, **options)

    def __hash__(self):
        """
        this method must be implemented in all subclasses
        to get the correct hash of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    def __eq__(self, other):
        """
        this method must be implemented in all subclasses to get the correct
        comparison between current and other permission for equality.

        :param PermissionBase other: other permission instance to be
                                     compared to the current one.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    def __ne__(self, other):
        """
        this method must be implemented in all subclasses to get the correct
        comparison between current and other permission for not equality.

        :param PermissionBase other: other permission instance to be
                                     compared to the current one.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
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
        """

        raise CoreNotImplementedError()

    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: CoreEntity
        """

        raise CoreNotImplementedError()

    def get_id(self):
        """
        gets permission id.
        note that this object must be fully unique for each different permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()
