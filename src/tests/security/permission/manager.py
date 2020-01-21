# -*- coding: utf-8 -*-
"""
permission manager module.
"""

import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.database.services import get_current_store
from pyrin.security.permission.manager import PermissionManager as BasePermissionManager
from pyrin.utils.sqlalchemy import entity_to_dict_list

from tests.security.permission.models import PermissionEntity


class PermissionManager(BasePermissionManager):
    """
    permission manager class.
    """

    def __init__(self):
        """
        initializes an instance of PermissionManager.
        """

        BasePermissionManager.__init__(self)

    def synchronize_all(self, **options):
        """
        synchronizes all permissions with database.
        it creates or updates the available permissions.
        """

        entities = [permission.to_entity() for permission in self.get_permissions()]
        needs_update = [entity for entity in entities if
                        self._exists(entity.primary_key()) is True]
        needs_insert = list(set(entities).difference(set(needs_update)))

        if needs_insert:
            self._bulk_insert(needs_insert)
        if needs_update:
            self._bulk_update(needs_update)

    def _exists(self, permission_id):
        """
        gets a value indicating that given permission exists in database.

        :param int permission_id: permission id.

        :rtype: bool
        """

        store = get_current_store()
        query = store.query(PermissionEntity.id).filter(PermissionEntity.id == permission_id)
        permission_count = sqlalchemy_utils.count(query)

        return permission_count > 0

    def _bulk_insert(self, entities):
        """
        bulk inserts the given permission entities.

        :param list[PermissionEntity] entities: permission entities to be inserted.
        """

        store = get_current_store()
        store.bulk_insert_mappings(PermissionEntity, entity_to_dict_list(entities, False))
        store.commit()

    def _bulk_update(self, entities):
        """
        bulk updates the given permission entities.

        :param list[PermissionEntity] entities: permission entities to be updated.
        """

        store = get_current_store()
        store.bulk_update_mappings(PermissionEntity, entity_to_dict_list(entities, False))
        store.commit()
