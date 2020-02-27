# -*- coding: utf-8 -*-
"""
permission manager module.
"""

from pyrin.core.context import Context, Manager
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.services import get_current_store
from pyrin.security.permission.base import PermissionBase
from pyrin.utils.sqlalchemy import entity_to_dict_list
from pyrin.security.permission.exceptions import InvalidPermissionTypeError, \
    DuplicatedPermissionError


class PermissionManager(Manager):
    """
    permission manager class.
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
            self._bulk_insert(needs_insert)
        if needs_update:
            self._bulk_update(needs_update)

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

    def _bulk_insert(self, entities):
        """
        bulk inserts the given permission entities.

        :param list[CoreEntity] entities: permission entities to be inserted.
        """

        if len(entities) > 0:
            store = get_current_store()
            store.bulk_insert_mappings(type(entities[0]), entity_to_dict_list(entities, False))
            store.commit()

    def _bulk_update(self, entities):
        """
        bulk updates the given permission entities.

        :param list[CoreEntity] entities: permission entities to be updated.
        """

        if len(entities) > 0:
            store = get_current_store()
            store.bulk_update_mappings(type(entities[0]), entity_to_dict_list(entities, False))
            store.commit()
