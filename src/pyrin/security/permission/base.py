# -*- coding: utf-8 -*-
"""
permission base module.
"""

from abc import abstractmethod

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

    @abstractmethod
    def __hash__(self):
        """
        this method must be implemented in all subclasses
        to get the correct hash of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: int
        """

        raise CoreNotImplementedError()

    @abstractmethod
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

    @abstractmethod
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

    @abstractmethod
    def __str__(self):
        """
        this method must be implemented in all subclasses to
        get the correct string representation of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def __repr__(self):
        """
        this method must be implemented in all subclasses to
        get the correct string representation of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: CoreEntity
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_id(self):
        """
        gets permission id.
        note that this object must be fully unique for each different permission.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()
