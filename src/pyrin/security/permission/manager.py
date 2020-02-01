# -*- coding: utf-8 -*-
"""
permission manager module.
"""

from pyrin.core.context import Context, Manager
from pyrin.security.permission.base import PermissionBase
from pyrin.security.permission.exceptions import InvalidPermissionTypeError, \
    DuplicatedPermissionError


class PermissionManager(Manager):
    """
    permission manager class.
    this class is intended to be an interface for top level application's permission
    package, so most methods of this class will raise CoreNotImplementedError.
    """

    def __init__(self):
        """
        initializes an instance of PermissionManager.
        """

        super().__init__()

        # holds a dict of all application's loaded permissions.
        # in the form of dict(str permission_id: PermissionBase permission)
        self.__permissions = Context()

    def register_permission(self, instance, **options):
        """
        registers the given permission.

        :param PermissionBase instance: permission instance to be registered.

        :raises InvalidPermissionTypeError: invalid permission type error.
        :raises DuplicatedPermissionError: duplicated permission error.
        """

        if not isinstance(instance, PermissionBase):
            raise InvalidPermissionTypeError('Input parameter [{instance}] is '
                                             'not an instance of PermissionBase.'
                                             .format(instance=str(instance)))

        if instance.get_id() in self.__permissions.keys():
            raise DuplicatedPermissionError('Permission [{permission}] has been '
                                            'already registered.'
                                            .format(permission=str(instance)))

        self.__permissions[instance.get_id()] = instance

    def get_permissions(self, **options):
        """
        gets all registered permissions.

        :rtype: list[PermissionBase]
        """

        return self.__permissions.values()

    def synchronize_all(self, **options):
        """
        synchronizes all permissions with database.
        it creates or updates the available permissions.
        if you don't need permissions in your application
        leave this method not implemented.
        """
        pass
