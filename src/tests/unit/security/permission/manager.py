# -*- coding: utf-8 -*-
"""
permission manager module.
"""

from pyrin.database.services import get_current_store
from pyrin.security.permission.manager import PermissionManager as BasePermissionManager

from tests.unit.security.permission import PermissionPackage
from tests.unit.security.permission.models import PermissionEntity


class PermissionManager(BasePermissionManager):
    """
    permission manager class.
    """

    package_class = PermissionPackage

    def _exists(self, permission_id):
        """
        gets a value indicating that given permission exists in database.

        :param int permission_id: permission id.

        :rtype: bool
        """

        store = get_current_store()
        permission_count = store.query(PermissionEntity.id).filter(PermissionEntity.id ==
                                                                   permission_id).count()

        return permission_count > 0
