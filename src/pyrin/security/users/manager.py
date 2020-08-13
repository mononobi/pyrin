# -*- coding: utf-8 -*-
"""
users manager module.
"""

from abc import abstractmethod

from pyrin.core.structs import Manager
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.users import UsersPackage


class UsersManager(Manager):
    """
    users manager class.
    this class is intended to provide some services needed in pyrin application.
    the top level application must extend this class considering business requirements.
    """

    package_class = UsersPackage

    @abstractmethod
    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param user: user to check its active status.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
