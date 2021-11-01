# -*- coding: utf-8 -*-
"""
authentication interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class AuthenticatorSingletonMeta(MultiSingletonMeta):
    """
    authenticator singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractAuthenticatorBase(CoreObject, metaclass=AuthenticatorSingletonMeta):
    """
    abstract authenticator base class.
    """

    @abstractmethod
    def authenticate(self, request, **options):
        """
        authenticates the user for given request.

        :param CoreRequest request: current request object.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def is_fresh(self):
        """
        gets a value indicating that current request has a fresh authentication.

        fresh authentication means an authentication which is done by providing
        user credentials to server.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def login(self, username, password, **options):
        """
        logs in a user with given info and stores/generates the relevant credentials.

        it may return the required credentials if they must be returned to client.

        :param str username: username.
        :param str password: password.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: required credentials.
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def logout(self, **options):
        """
        logouts the current user and clears its relevant credentials.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def name(self):
        """
        gets the name of this authenticator.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()
