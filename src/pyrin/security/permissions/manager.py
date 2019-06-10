# -*- coding: utf-8 -*-
"""
permissions manager module.
"""

from pyrin.core.context import CoreObject, Context
from pyrin.security.permissions.base import PermissionBase
from pyrin.security.permissions.exceptions import InvalidPermissionTypeError, \
    InvalidPermissionIDError, DuplicatedPermissionError, PermissionNotFoundError


class PermissionsManager(CoreObject):
    """
    permissions manager class.
    this class is intended to be an interface for top level application's permissions
    package, so most methods of this class will raise CoreNotImplementedError.
    """

    def __init__(self):
        """
        initializes an instance of PermissionsManager.
        """

        CoreObject.__init__(self)

        # holds a dict of all application's loaded permissions.
        # in the form of dict(permission_id: PermissionBase)
        self.__permissions = Context()

    def register_permission(self, instance, **options):
        """
        registers the given permission.

        :param PermissionBase instance: permission instance to be registered.

        :raises InvalidPermissionTypeError: invalid permission type error.
        :raises InvalidPermissionIDError: invalid permission id error.
        :raises DuplicatedPermissionError: duplicated permission error.
        """

        if not isinstance(instance, PermissionBase):
            raise InvalidPermissionTypeError('Input parameter [{instance}] is '
                                             'not an instance of PermissionBase.'
                                             .format(instance=str(instance)))

        if instance.get_id() is None:
            raise InvalidPermissionIDError('Permission [{instance}] has invalid id.'
                                           .format(instance=str(instance)))

        if instance.get_id() in self.__permissions.keys():
            raise DuplicatedPermissionError('Permission [{instance}] has been '
                                            'already registered.'
                                            .format(instance=str(instance)))

        self.__permissions[instance.get_id()] = instance
        instance.synchronize(**options)

    def _get_permissions(self):
        """
        gets all registered permissions.

        :rtype: list[PermissionBase]
        """

        return self.__permissions.values()

    def _get_permission(self, permission_id, **options):
        """
        gets the specified permission with given permission id.

        :param object permission_id: permission id.
                                     it must be an immutable type
                                     to be usable as dict key.

        :raises PermissionNotFoundError: permission not found error.

        :rtype: PermissionBase
        """

        if permission_id not in self.__permissions.keys():
            raise PermissionNotFoundError('Permission [{permission_id}] not found.'
                                          .format(permission_id=permission_id))

        return self.__permissions[permission_id]
