# -*- coding: utf-8 -*-
"""
permission base module.
"""

from abc import abstractmethod

import pyrin.security.permission.services as permission_services

from pyrin.core.structs import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class PermissionBase(CoreObject):
    """
    permission base class.

    all application permissions must be subclassed from this.
    """

    def __init__(self, *args, **options):
        """
        initializes an instance of PermissionBase.

        input parameters of this method in subclasses must be
        customized based on application's design requirements.
        """

        super().__init__()
        permission_services.register_permission(self, **options)

    def __hash__(self):
        """
        gets the hash value of current permission.

        :rtype: int
        """

        return hash(self.get_id())

    def __eq__(self, other):
        """
        gets the comparison between current and other permission for equality.

        :param PermissionBase other: other permission instance to be
                                     compared to the current one.

        :rtype: bool
        """

        if not isinstance(other, PermissionBase):
            return False

        return other.get_id() == self.get_id()

    def __ne__(self, other):
        """
        gets the comparison between current and other permission for not equality.

        :param PermissionBase other: other permission instance to be
                                     compared to the current one.

        :rtype: bool
        """

        return not self == other

    @abstractmethod
    def __str__(self):
        """
        gets the string representation of current permission.

        this method must be implemented in subclasses.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def __repr__(self):
        """
        gets the string representation of current permission.

        :rtype: str
        """

        return str(self)

    @abstractmethod
    def to_entity(self):
        """
        gets the equivalent entity of current permission.

        this method must be implemented in subclasses.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: BaseEntity
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def get_id(self):
        """
        gets permission id.

        this method must be implemented in subclasses.
        it could return a single value or a combination of multiple values
        (ex. a tuple). note that the returned value must be fully unique for
        each different permission and also it must be a hashable value to
        be used as dict key.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()
