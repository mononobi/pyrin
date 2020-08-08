# -*- coding: utf-8 -*-
"""
permission models module.
"""

from sqlalchemy import Unicode, SmallInteger

from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn


class PermissionBaseEntity(CoreEntity):
    """
    permission base entity class.
    """

    _table = 'permission'

    id = CoreColumn(name='id', type_=SmallInteger, primary_key=True, nullable=False, index=True)


class PermissionEntity(PermissionBaseEntity):
    """
    permission entity class.
    """

    _extend_existing = True

    description = CoreColumn(name='description', type_=Unicode(100), nullable=False)
