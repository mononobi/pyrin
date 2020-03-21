# -*- coding: utf-8 -*-
"""
permission models module.
"""

from sqlalchemy import Unicode, SmallInteger

from pyrin.core.structs import DTO
from pyrin.database.model.base import CoreEntity
from pyrin.database.orm.sql.schema.base import CoreColumn


class PermissionBaseEntity(CoreEntity):
    """
    permission base entity class.
    """

    __tablename__ = 'permission'

    id = CoreColumn(name='id', type_=SmallInteger, primary_key=True, nullable=False, index=True)


class PermissionEntity(PermissionBaseEntity):
    """
    permission entity class.
    """

    __table_args__ = DTO(extend_existing=True)

    description = CoreColumn(name='description', type_=Unicode(100), nullable=False)
