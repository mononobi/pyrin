# -*- coding: utf-8 -*-
"""
authorization interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class AuthorizerSingletonMeta(MultiSingletonMeta):
    """
    authorizer singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractAuthorizerBase(CoreObject, metaclass=AuthorizerSingletonMeta):
    """
    abstract authorizer base class.
    """

    @abstractmethod
    def authorize(self, user, permissions, **options):
        """
        authorizes the given user for specified permissions.

        if user does not have each one of the specified
        permissions, an error will be raised.

        :param user: user identity to authorize permissions for.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for user authorization.

        :keyword dict user_info: user info to be used for authorization.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def is_superuser(self):
        """
        gets a value indicating that the current user is superuser.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this authorizer.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()
