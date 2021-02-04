# -*- coding: utf-8 -*-
"""
permission manager module.
"""

from abc import abstractmethod

import pyrin.database.bulk.services as bulk_services

from pyrin.core.globals import SECURE_FALSE
from pyrin.core.structs import Context, Manager
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.permission import PermissionPackage
from pyrin.security.permission.base import PermissionBase
from pyrin.security.permission.exceptions import InvalidPermissionTypeError, \
    DuplicatedPermissionError


class PermissionManager(Manager):
    """
    permission manager class.
    """

    package_class = PermissionPackage

    def __init__(self):
        """
        initializes an instance of PermissionManager.
        """

        super().__init__()

        # holds a dict of all application's loaded permissions.
        # in the form of dict[object permission_id: PermissionBase instance]
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
                                             'not an instance of [{base}].'
                                             .format(instance=instance,
                                                     base=PermissionBase))

        if instance.get_id() in self.__permissions:
            raise DuplicatedPermissionError('Permission [{permission}] has been '
                                            'already registered.'
                                            .format(permission=instance))

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
        """

        entities = [permission.to_entity() for permission in self.get_permissions()]
        needs_update = [entity for entity in entities if
                        self._exists(*entity.primary_key(as_tuple=True)) is True]
        needs_insert = list(set(entities).difference(set(needs_update)))

        if needs_insert:
            bulk_services.insert(*needs_insert, readable=SECURE_FALSE)
        if needs_update:
            bulk_services.update(*needs_update, readable=SECURE_FALSE)

    @abstractmethod
    def _exists(self, *primary_key):
        """
        gets a value indicating that given permission exists in database.

        this method must be implemented in subclasses, the input value
        could be as many as needed arguments to represent the primary key
        of your permission entity.
        if you don't want to use permissions concept in your application,
        you could leave this method unimplemented.

        :param object primary_key: permission primary key value.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
